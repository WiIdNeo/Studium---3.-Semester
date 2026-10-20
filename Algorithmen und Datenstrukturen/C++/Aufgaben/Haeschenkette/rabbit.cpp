#include "rabbit.hpp"

rabbit::rabbit(int ears, std::string _name) {
    age_in_weeks = 0;
    name = _name;
    num_of_ears = ears;
    weight_in_gramms = 100;
    eatable = false;
}

void rabbit::set_eatable() {
    age_in_weeks < 13 && age_in_weeks > 8 
    && weight_in_gramms <= 2000 && weight_in_gramms >= 1500
    ? eatable = true 
    : eatable = false;
}

void rabbit::age() {
    ++age_in_weeks;
    set_eatable();
}

void rabbit::feed() {
    weight_in_gramms = weight_in_gramms + (float)randm(gen);
    set_eatable();
}

int rabbit::request_age() { 
    return age_in_weeks; 
}

float rabbit::request_weight() { 
    return weight_in_gramms; 
}

rabbit::~rabbit() {}


