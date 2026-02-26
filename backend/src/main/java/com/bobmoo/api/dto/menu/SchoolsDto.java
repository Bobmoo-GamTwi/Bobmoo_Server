package com.bobmoo.api.dto.menu;

import lombok.AllArgsConstructor;
import lombok.Getter;

import java.util.List;

@Getter
@AllArgsConstructor
public class SchoolsDto {
    private String schoolName;
    private List<CafeteriaDto> cafeterias;
}
