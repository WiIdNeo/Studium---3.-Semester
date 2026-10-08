#include <malloc.h>
#include <iostream>

class string {
    public:
        string() {
            text = (char*)malloc(1);
            text[0] = '\0';
            laenge = 1;
        };
        string(const char* data) { 
            if (data == nullptr) { // kann man das auch per goto Lösen? Oder geht das nicht, weil der Data pointer verloren geht?
                text = (char*)malloc(1);
                text[0] = '\0';
                laenge = 0;
            }
            else {
            laenge = count(data);
            text = (char*)malloc(laenge + 1);
            int i = 0;
            while (i < laenge) {
                text[i] = data[i];
                i++;
            }
            text[i] = '\0';
            }
        }
        char* data() {
            return text;
        }
        void clear() {
            free(text); // Theoretischer sicherer wäre 
            text = (char*)malloc(1); // realloc(text, 1)
            text[0] = '\0';
            laenge = 0;
        }
        void print() {
            std::cout << text;
        }
        int find(char c) {
            for (int j = 0; j < laenge; j++) {
                if (text[j] == c) {
                    return j;
                }
            }
            return -1;
        }
        void append(const char* data) {
            int add_laenge = count(data);      // count liefert bei nullptr 0
            if (add_laenge == 0) {
                return;                           // nichts anzuhängen
            }

            if (data == text) {                   // Selbst-Anhängen
                string tmp(data);                 // Kopie über den Konstruktor
                append(tmp.data());               // tmp ist ein anderer Puffer
                return;                           // Destruktor von tmp gibt ihn frei
            }

            char* neu = (char*)realloc(text, laenge + add_laenge + 1);
            if (neu == nullptr) {
                return;                           // text bleibt gültig
            }
            text = neu;

            for (int i = 0; i < add_laenge; i++) {
                text[laenge + i] = data[i];
            }
            laenge = laenge + add_laenge;
            text[laenge] = '\0';
        }
        ~string() {
            free(text);
        }

    private:
        char* text; 
        int laenge;

        int count(const char* data) {
            laenge = 0;
            if (data == nullptr) {
                return 0;
            }
            while (data[laenge] != '\0') {
                laenge++;
            }
            return laenge;
        }
};