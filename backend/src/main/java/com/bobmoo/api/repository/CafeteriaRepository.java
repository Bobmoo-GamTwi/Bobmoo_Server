package com.bobmoo.api.repository;

import com.bobmoo.api.domain.Cafeteria;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Collection;
import java.util.List;

public interface CafeteriaRepository extends JpaRepository<Cafeteria,Long> {
    List<Cafeteria> findByNameIn(Collection<String> names);
}
