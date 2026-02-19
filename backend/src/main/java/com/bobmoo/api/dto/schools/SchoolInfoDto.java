package com.bobmoo.api.dto.schools;

import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public class SchoolInfoDto {
    private int schoolId;
    private String schoolName;
    private String schoolColor;
}
