package com.bobmoo.api.domain;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.time.LocalDate;

@Entity
@Getter
@NoArgsConstructor
public class Meal {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private LocalDate date;

    @Column(nullable = false)
    private String school;

    @Column(nullable = false)
    private String cafeteriaName;

    @Enumerated(EnumType.STRING)
    private MealTime mealTime;

    private String course;

    @Column(nullable = false, columnDefinition = "TEXT")
    private String mainMenu;

    private int price;
}
