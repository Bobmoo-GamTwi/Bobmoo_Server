package com.bobmoo.api.controller;

import com.bobmoo.api.common.ResponseStatus;
import com.bobmoo.api.dto.schools.SchoolInfoDto;
import com.bobmoo.api.dto.schools.SchoolResponse;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/v1/schools")
public class SchoolController {

    @GetMapping
    public SchoolResponse getSchools(){

        List<SchoolInfoDto> mockSchools = List.of(
                new SchoolInfoDto(1, "inha", "005BAC"),
                new SchoolInfoDto(2, "chonnum", "006B3F")
        );

        return new SchoolResponse(ResponseStatus.SUCCESS, mockSchools);
    }
}