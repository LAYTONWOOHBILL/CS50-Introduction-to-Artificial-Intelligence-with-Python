import csv
import itertools
import sys

PROBS = {
    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },
    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },
    # Mutation probability
    "mutation": 0.01
}


def main():
    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)

    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any((people[person]["trait"] is not None
                              and people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):
                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    [set(), {'Harry'}, {'James'}, {'Lily'}, {'Harry', 'James'}, {'Harry', 'Lily'}, {'James', 'Lily'}, {'Harry', 'James', 'Lily'}]
    [set(), {'Harry'}, {'James'}, {'Lily'}, {'Harry', 'James'}, {'Harry', 'Lily'}, {'James', 'Lily'}, {'Harry', 'James', 'Lily'}]
    [set(), {'Harry'}, {'James'}, {'Lily'}, {'Harry', 'James'}, {'Harry', 'Lily'}, {'James', 'Lily'}, {'Harry', 'James', 'Lily'}]
    [set(), {'James'}, {'Lily'}, {'James', 'Lily'}]
    [set(), {'Harry'}, {'Lily'}, {'Harry', 'Lily'}]
    [set(), {'Harry'}, {'James'}, {'Harry', 'James'}]
    [set(), {'Lily'}]
    [set(), {'James'}]
    [set(), {'Harry'}]
    [set()]
    [set(), {'Harry'}, {'James'}, {'Lily'}, {'Harry', 'James'}, {'Harry', 'Lily'}, {'James', 'Lily'}, {'Harry', 'James', 'Lily'}]
    [set(), {'Harry'}, {'James'}, {'Lily'}, {'Harry', 'James'}, {'Harry', 'Lily'}, {'James', 'Lily'}, {'Harry', 'James', 'Lily'}]
    [set(), {'James'}, {'Lily'}, {'James', 'Lily'}]
    [set(), {'Harry'}, {'Lily'}, {'Harry', 'Lily'}]
    [set(), {'Harry'}, {'James'}, {'Harry', 'James'}]
    [set(), {'Lily'}]
    [set(), {'James'}]
    [set(), {'Harry'}]
    [set()]
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """

    joint_prob = 1

    for person, person_description in people.items():
        # Set person gene
        # everyone not in `one_gene` or `two_gene` does not have the gene
        person_gene = 0
        # everyone in set `one_gene` has one copy of the gene
        if person in one_gene:
            person_gene = 1
        # everyone in set `two_genes` has two copies of the gene
        elif person in two_genes:
            person_gene = 2

        # Set person trait
        person_trait = False
        if person in have_trait:
            person_trait = True

        # For anyone with no parents listed in the data set,
        # use the probability distribution PROBS["gene"] to determine the probability that they have a particular number of the gene.
        # print(person, person_description)
        if not person_description["mother"] and not person_description["father"]:
            parents_gene_prob = PROBS["gene"][person_gene]

        # For anyone with parents in the data set, each parent will pass one of their two genes on to their child randomly,
        # and there is a PROBS["mutation"] chance that it mutates (goes from being the gene to not being the gene, or vice versa).
        else:
            # Mother Mutated Gene Probability
            mother_mutated_prob = PROBS["mutation"]
            if person_description["mother"] in one_gene:
                mother_mutated_prob = 0.5 * (1 - PROBS["mutation"])
            elif person_description["mother"] in two_genes:
                mother_mutated_prob = 1 - PROBS["mutation"]

            # Father Mutated Gene Probability
            father_mutated_prob = PROBS["mutation"]
            if person_description["father"] in one_gene:
                father_mutated_prob = 0.5 * (1 - PROBS["mutation"])
            elif person_description["father"] in two_genes:
                father_mutated_prob = 1 - PROBS["mutation"]

            # Person Mutated Gene Probability
            if person in one_gene:
                # one gene pass -> (mother_mutated, no father_mutated) OR (no mother_mutated, father_mutated)
                parents_gene_prob = (mother_mutated_prob * (1 - father_mutated_prob)) + (father_mutated_prob * (1 - mother_mutated_prob))

            elif person in two_genes:
                # two pass -> mother_mutated, father_mutated
                parents_gene_prob = mother_mutated_prob * father_mutated_prob
            else:
                # not pass
                parents_gene_prob = (1 - mother_mutated_prob) * (1 - father_mutated_prob)

        # print(person, parents_gene_prob, PROBS["trait"][person_gene][person_trait])

        person_prob = parents_gene_prob * PROBS["trait"][person_gene][person_trait]
        joint_prob *= person_prob

    return joint_prob


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        # Set person gene
        # everyone not in `one_gene` or `two_gene` does not have the gene
        person_gene = 0
        # everyone in set `one_gene` has one copy of the gene
        if person in one_gene:
            person_gene = 1
        # everyone in set `two_genes` has two copies of the gene
        elif person in two_genes:
            person_gene = 2

        # Set person trait
        person_trait = False
        if person in have_trait:
            person_trait = True

        probabilities[person]["gene"][person_gene] += p
        probabilities[person]["trait"][person_trait] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    {'Harry': {'gene': {2: 0.000289561041, 1: 0.014421060318, 0: 0.017106968641}, 'trait': {True: 0.008435078141140003, False: 0.02338251185885999}},
    'James': {'gene': {2: 0.006286149999999998, 1: 0.016247280000000003, 0: 0.009284159999999993}, 'trait': {True: 0.031817589999999986, False: 0}},
    'Lily': {'gene': {2: 0.00011515000000000002, 1: 0.00043428000000000005, 0: 0.031268159999999996}, 'trait': {True: 0, False: 0.031817589999999986}}}
    """

    for person in probabilities:
        gene_sum = sum(probabilities[person]["gene"].values())
        trait_sum = sum(probabilities[person]["trait"].values())

        for gene in probabilities[person]["gene"]:
            probabilities[person]["gene"][gene] /= gene_sum
        for trait in probabilities[person]["trait"]:
            probabilities[person]["trait"][trait] /= trait_sum


if __name__ == "__main__":
    main()
