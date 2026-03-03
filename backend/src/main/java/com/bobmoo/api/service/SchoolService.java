package com.bobmoo.api.service;

import com.bobmoo.api.controller.SchoolController;
import com.bobmoo.api.dto.schools.SchoolInfoDto;
import com.bobmoo.api.dto.schools.SchoolResponse;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
public class SchoolService {

    private final List<SchoolInfoDto> mockSchools;

    //후에 db에서 값을 가져오도록 수정
    public SchoolService(){
        mockSchools = List.of(
                new SchoolInfoDto(1, "inha", "인하대학교", "005BAC"),
                new SchoolInfoDto(2, "chonnum", "전남대학교", "006B3F")
        );
    }

    public List<SchoolInfoDto> getAllSchools() {
        return mockSchools;
    }

    public List<SchoolInfoDto> findSchoolByName(String name){
        List<SchoolInfoDto> res = new ArrayList<>();
        for (SchoolInfoDto school : mockSchools){
            if (school.getSchoolNameK().contains(name)){
                res.add(school);
            }
        }
        return res;
    }
}
