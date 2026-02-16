package com.bobmoo.api.dto;

import lombok.AllArgsConstructor;
import lombok.Getter;

import java.time.LocalDate;
import java.util.List;

@Getter
@AllArgsConstructor
public class MenuResponse {
    private LocalDate date;
    private String school;
    private List<CafeteriaDto> cafeterias;
}
