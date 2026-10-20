#ifndef RABBIT_HPP
#define RABBIT_HPP

#include <iostream>
#include <string>
#include <random>

class rabbit {
    public:
        bool eatable;
        rabbit(int num_of_ears, std::string name);
        void age();
        void feed();
        int request_age();
        float request_weight();

    private:
        void set_eatable();

        std::string name;
        int age_in_weeks;
        float weight_in_gramms;
        int num_of_ears;
        std::mt19937 gen{std::random_device{}()};
        std::uniform_real_distribution<float> randm{10.0f, 200.0f};
};
#endif



