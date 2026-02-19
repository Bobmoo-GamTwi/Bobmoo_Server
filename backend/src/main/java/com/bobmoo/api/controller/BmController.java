package com.bobmoo.api.controller;

import com.bobmoo.api.dto.MenuResponse;
import com.bobmoo.api.service.MealService;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.time.LocalDate;

@RestController
@RequestMapping("/api/v1/menu")
public class BmController {

    // 1. MealService를 주입받습니다.
    private final MealService mealService;

    public BmController(MealService mealService) {
        this.mealService = mealService;
    }

    // 2. 서비스 메소드를 호출합니다.
    @GetMapping("/today")
    public MenuResponse getTodayMeals() {
        // 컨트롤러는 서비스를 호출하고 결과를 반환하는 역할만 합니다.
        return mealService.findMealsByDate(LocalDate.now());
    }

    @GetMapping
    public MenuResponse getMealsByDate(
            @RequestParam("date") @DateTimeFormat(pattern = "yyyy-MM-dd") LocalDate date) {
        return mealService.findMealsByDate(date);
    }

}
