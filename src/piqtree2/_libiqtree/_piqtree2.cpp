// #include <main/libiqtree2_fun.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <iostream>
#include <string>
#include <vector>

extern "C" {
    // Declaration of the new C wrapper function
    const char* build_tree(const char** names, const char** seqs, int names_size, int seqs_size, const char* model, int rand_seed);
    void free_result(const char* result);
}

using namespace std;

namespace py = pybind11;

// Calculates the robinson fould distance between two trees
extern int robinson_fould(const string& tree1, const string& tree2);

// Generates a set of random phylogenetic trees
// tree_gen_mode allows:"YULE_HARDING", "UNIFORM", "CATERPILLAR", "BALANCED",
// "BIRTH_DEATH", "STAR_TREE"
extern string random_tree(int num_taxa,
                          string tree_gen_mode,
                          int num_trees,
                          int rand_seed);

// Perform phylogenetic analysis on the input alignment (in string format)
// With estimation of the best topology
std::string iq_build_tree(const std::vector<std::string>& names,
                           const std::vector<std::string>& seqs,
                           const std::string& model,
                           int rand_seed) {
    // Convert the input vectors to C-style arrays for C wrapper
    const char* names_arr[names.size()];
    const char* seqs_arr[seqs.size()];

    for (size_t i = 0; i < names.size(); ++i) {
        names_arr[i] = names[i].c_str();
    }

    for (size_t i = 0; i < seqs.size(); ++i) {
        seqs_arr[i] = seqs[i].c_str();
    }

    // Call the C function
    const char* result = build_tree(names_arr, seqs_arr, names.size(), seqs.size(), model.c_str(), rand_seed);

    // Make sure to copy the C-string result to a std::string (as Python expects a std::string)
    std::string result_str(result);

    // Free the allocated result string
    free_result(result);

    return result_str;
}

// Perform phylogenetic analysis on the input alignment (in string format)
// With restriction to the input toplogy
extern string fit_tree(vector<string>& names,
                       vector<string>& seqs,
                       string model,
                       string intree,
                       int rand_seed);

int mine() {
  return 42;
}

PYBIND11_MODULE(_piqtree2, m) {
  m.doc() = "piqtree2 - Unlock the Power of IQ-TREE2 with Python!";

  m.def("iq_robinson_fould", &robinson_fould,
        "Calculates the robinson fould distance between two trees");
  m.def("iq_random_tree", &random_tree,
        "Generates a set of random phylogenetic trees. tree_gen_mode "
        "allows:\"YULE_HARDING\", \"UNIFORM\", \"CATERPILLAR\", \"BALANCED\", "
        "\"BIRTH_DEATH\", \"STAR_TREE\".");
  m.def("iq_build_tree", &iq_build_tree,
        "Perform phylogenetic analysis on the input alignment (in string "
        "format). With estimation of the best topology.");
  m.def("iq_fit_tree", &fit_tree,
        "Perform phylogenetic analysis on the input alignment (in string "
        "format). With restriction to the input toplogy.");
  m.def("mine", &mine, "The meaning of life, the universe (and everything)!");
}
