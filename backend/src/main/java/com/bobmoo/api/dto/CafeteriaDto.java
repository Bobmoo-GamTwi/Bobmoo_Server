package com.bobmoo.api.dto;

import lombok.AllArgsConstructor;
import lombok.Getter;

import java.util.List;
import java.util.Map;

@Getter
@AllArgsConstructor
public class CafeteriaDto {
    private String name;
    private OperatingHoursDto hours;
    private Map<String, List<MenuDto>> meals;
}
