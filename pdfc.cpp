#include <poppler/PopplerDocument.h>
#include <poppler/PopplerPage.h>
#include <iostream>
#include <fstream>

int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cerr << "Usage: " << argv[0] << " <input.pdf> <output.txt>" << std::endl;
        return 1;
    }

    const char* input_pdf = argv[1];
    const char* output_txt = argv[2];

    // Initialize Poppler
    poppler::document* doc = poppler::document::load_from_file(input_pdf);
    if (!doc) {
        std::cerr << "Error: Could not open PDF file " << input_pdf << std::endl;
        return 1;
    }

    std::ofstream out(output_txt);
    if (!out) {
        std::cerr << "Error: Could not open output file " << output_txt << std::endl;
        return 1;
    }

    // Extract text from each page
    int num_pages = doc->pages();
    for (int i = 0; i < num_pages; ++i) {
        poppler::page* pg = doc->create_page(i);
        if (pg) {
            std::string text = pg->text().to_utf8();
            out << text << std::endl;
            delete pg;
        }
    }

    delete doc;
    out.close();

    std::cout << "Text extraction complete." << std::endl;
    return 0;
}