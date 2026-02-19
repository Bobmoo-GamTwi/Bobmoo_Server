package com.bobmoo.api.repository;

import com.bobmoo.api.domain.Meal;
import org.springframework.data.jpa.repository.JpaRepository;

import java.time.LocalDate;
import java.util.List;

public interface MealRepository extends JpaRepository<Meal,Long> {
    public List<Meal> findByDate(LocalDate date);
}
