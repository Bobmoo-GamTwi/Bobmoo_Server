package com.bobmoo.api.dto;

import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public class MenuDto {
    private String course;
    private String mainMenu;
    private int price;
}
