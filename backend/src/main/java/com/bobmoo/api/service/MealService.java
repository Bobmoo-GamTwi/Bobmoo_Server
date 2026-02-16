package com.bobmoo.api.service;

import com.bobmoo.api.domain.Cafeteria;
import com.bobmoo.api.domain.Meal;
import com.bobmoo.api.dto.CafeteriaDto;
import com.bobmoo.api.dto.MenuDto;
import com.bobmoo.api.dto.MenuResponse;
import com.bobmoo.api.dto.OperatingHoursDto;
import com.bobmoo.api.repository.CafeteriaRepository;
import com.bobmoo.api.repository.MealRepository;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
public class MealService {

    private final MealRepository mealRepository;
    private final CafeteriaRepository cafeteriaRepository;

    public MealService(MealRepository mealRepository,  CafeteriaRepository cafeteriaRepository) {
        this.mealRepository = mealRepository;
        this.cafeteriaRepository = cafeteriaRepository;
    }

    public MenuResponse findMealsByDate(LocalDate date){
        // 1. DB에서 해당 날짜의 모든 Meal 엔티티를 가져옵니다.
        List<Meal> mealsFromDb = mealRepository.findByDate(date);

        // 만약 그날 메뉴가 하나도 없다면, 빈 응답을 보냅니다.
        if (mealsFromDb.isEmpty()) {
            // TODO: 학교 이름도 동적으로 처리할 필요가 있음 (예: 파라미터로 받기)
            return new MenuResponse(date, "학교 정보 없음", new ArrayList<>());
        }

        // 2. 첫 번째 메뉴에서 학교 이름을 가져옵니다.
        String schoolName = mealsFromDb.get(0).getSchool();

        // 3. 가져온 Meal 리스트를 식당 이름(cafeteriaName)으로 그룹핑합니다.
        Map<String, List<Meal>> mealsByCafeteriaName = mealsFromDb.stream()
                .collect(Collectors.groupingBy(Meal::getCafeteriaName));        // 3. 그룹핑된 Map을 최종 DTO 형태로 변환합니다.
        // Step A: 조회된 메뉴들에 해당하는 식당 이름 목록을 추출합니다.
        List<String> cafeteriaNames = new ArrayList<>(mealsByCafeteriaName.keySet());

        // Step B: 한 번의 쿼리로 모든 식당 정보를 가져옵니다 (N+1 문제 방지).
        List<Cafeteria> cafeteriaEntities = cafeteriaRepository.findByNameIn(cafeteriaNames);

        // Step C: 이름으로 쉽게 찾을 수 있도록 Map으로 변환합니다.
        Map<String, Cafeteria> cafeteriaMap = cafeteriaEntities.stream()
                .collect(Collectors.toMap(Cafeteria::getName, cafeteria -> cafeteria));

        // Step D: 최종 DTO를 조립할 때, 위에서 만든 Map에서 식당 정보를 찾아 사용합니다.
        List<CafeteriaDto> cafeteriaDtos = mealsByCafeteriaName.entrySet().stream()
                .map(entry -> {
                    String cafeteriaName = entry.getKey();
                    List<Meal> meals = entry.getValue();

                    // Map에서 해당 식당의 엔티티를 찾습니다.
                    Cafeteria cafeteria = cafeteriaMap.get(cafeteriaName);


                    // 3-1. 식당별 메뉴 리스트를 다시 아침/점심/저녁으로 그룹핑합니다.
                    //      이때 Meal 엔티티를 MenuDto로 변환합니다.
                    Map<String, List<MenuDto>> mealsByTime = meals.stream()
                            .collect(Collectors.groupingBy(
                                    meal -> meal.getMealTime().name().toLowerCase(), // "BREAKFAST" -> "breakfast"
                                    Collectors.mapping(
                                            meal -> new MenuDto(meal.getCourse(), meal.getMainMenu(), meal.getPrice()),
                                            Collectors.toList()
                                    )
                            ));

                    // 실제 DB에서 가져온 운영 시간 정보로 DTO를 생성합니다.
                    OperatingHoursDto hours = new OperatingHoursDto(
                            cafeteria.getBreakfastHours(),
                            cafeteria.getLunchHours(),
                            cafeteria.getDinnerHours()
                    );

                    return new CafeteriaDto(cafeteriaName, hours, mealsByTime);
                })
                .collect(Collectors.toList());

        // 5. 최종 DailyMenuResponse DTO를 조립할 때, 하드코딩 대신 변수를 사용합니다.
        return new MenuResponse(date, schoolName, cafeteriaDtos);
        }
    }


