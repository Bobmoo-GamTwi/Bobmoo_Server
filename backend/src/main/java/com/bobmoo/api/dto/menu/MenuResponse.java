package com.bobmoo.api.dto.menu;

import lombok.AllArgsConstructor;
import lombok.Getter;

import java.time.LocalDate;
import java.util.List;

@Getter
@AllArgsConstructor
public class MenuResponse {
    private LocalDate date;
    private SchoolsDto schools;
}
