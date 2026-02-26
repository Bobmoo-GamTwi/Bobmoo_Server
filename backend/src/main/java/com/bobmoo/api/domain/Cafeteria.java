package com.bobmoo.api.domain;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Entity
@Getter
@NoArgsConstructor
public class Cafeteria {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String name;

    //후에 @ManyToOne, @OneToMany를 써서 정규화 리팩토링 가능
    @Column(nullable = false)
    private String school;

    private  String breakfastHours;
    private  String lunchHours;
    private  String dinnerHours;
}
