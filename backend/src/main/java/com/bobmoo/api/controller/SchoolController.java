package com.bobmoo.api.controller;

import com.bobmoo.api.common.ResponseStatus;
import com.bobmoo.api.dto.MenuResponse;
import com.bobmoo.api.dto.schools.SchoolInfoDto;
import com.bobmoo.api.dto.schools.SchoolResponse;
import com.bobmoo.api.service.SchoolService;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.time.LocalDate;
import java.util.List;

@RestController
@RequestMapping("/api/v1/schools")
public class SchoolController {

    private final SchoolService schoolService;

    public SchoolController(SchoolService SchoolService) { this.schoolService = SchoolService; }

    @GetMapping
    public SchoolResponse getSchools(
            @RequestParam(value = "school", required = false) String school
    ){
        if (school == null){
            return new SchoolResponse(ResponseStatus.SUCCESS, schoolService.getAllSchools());
        }

        List<SchoolInfoDto> found = schoolService.findSchoolByName(school);

        if (found.isEmpty()) {
            return new SchoolResponse(ResponseStatus.FAIL, List.of());
        }
        return new SchoolResponse(ResponseStatus.SUCCESS, found);

    }
}