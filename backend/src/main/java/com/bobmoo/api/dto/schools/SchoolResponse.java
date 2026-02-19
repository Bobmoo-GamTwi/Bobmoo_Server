package com.bobmoo.api.dto.schools;

import com.bobmoo.api.common.ResponseStatus;
import lombok.AllArgsConstructor;
import lombok.Getter;

import java.util.List;

@Getter
@AllArgsConstructor
public class SchoolResponse {
    private ResponseStatus status;
    private List<SchoolInfoDto> data;
}
