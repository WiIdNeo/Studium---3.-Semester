#include <iostream>
#include <random>
#include <string>

class Rabbit {
public:
    Rabbit(std::string name, int num_ears)
        : name(std::move(name)), num_ears(num_ears) {}

    void feed() {
        std::uniform_int_distribution<int> dist(10, 200); // 10 bis 200 g Zunahme
        weight_gramms += dist(gen);
        update_eatable();
    }

    void age() {
        ++age_weeks;
        update_eatable();
    }

    int get_age_weeks() const { return age_weeks; }
    int get_weight_gramms() const { return weight_gramms; }
    bool is_eatable() const { return eatable; }

private:
    void update_eatable() {
        bool right_age    = age_weeks >= 9 && age_weeks <= 12;
        bool right_weight = weight_gramms >= 1500 && weight_gramms <= 2000;
        eatable = right_age && right_weight;
    }

    std::string name;
    int num_ears;
    int age_weeks = 0;
    int weight_gramms = 100;
    bool eatable = false;

    // Zufallsgenerator nur einmal für alle Hasen erzeugen
    inline static std::mt19937 gen{std::random_device{}()};
};

int main() {
    Rabbit rabbit1("Hase1", 2);
    for (int i = 0; i < 14; ++i) {
        std::cout << "Woche " << rabbit1.get_age_weeks()
                  << ": " << rabbit1.get_weight_gramms() << " g"
                  << (rabbit1.is_eatable() ? " (essbar)" : "") << '\n';
        rabbit1.age();
        rabbit1.feed();
    }
}