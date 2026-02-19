package com.bobmoo.api.dto;

import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public class OperatingHoursDto {
    private String breakfast;
    private String lunch;
    private String dinner;
}
