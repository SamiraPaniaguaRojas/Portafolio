package com.gomez.apiAcademico.model;

import jakarta.persistence.*;
import jakarta.validation.constraints.*;
import java.time.LocalDate;

@Entity
public class Docente {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long idDocente;

    @NotBlank
    private String nomDocente;

    @NotBlank
    private String dirDocente;

    @NotBlank
    private String ciuDocente;

    @Email
    @NotBlank
    private String emailDocente;

    @Past
    @NotNull
    private LocalDate fecNacimiento;

    @Min(0)
    private int tiempoServicio;

    // Getters y Setters
    public Long getIdDocente() {
        return idDocente;
    }

    public void setIdDocente(Long idDocente) {
        this.idDocente = idDocente;
    }
    public String getNomDocente() {
        return nomDocente;
    }

    public void setNomDocente(String nomDocente) {
        this.nomDocente = nomDocente;
    }

    public String getDirDocente() {
        return dirDocente;
    }

    public void setDirDocente(String dirDocente) {
        this.dirDocente = dirDocente;
    }

    public String getCiuDocente() {
        return ciuDocente;
    }

    public void setCiuDocente(String ciuDocente) {
        this.ciuDocente = ciuDocente;
    }

    public String getEmailDocente() {
        return emailDocente;
    }

    public void setEmailDocente(String emailDocente) {
        this.emailDocente = emailDocente;
    }

    public LocalDate getFecNacimiento() {
        return fecNacimiento;
    }

    public void setFecNacimiento(LocalDate fecNacimiento) {
        this.fecNacimiento = fecNacimiento;
    }

    public int getTiempoServicio() {
        return tiempoServicio;
    }

    public void setTiempoServicio(int tiempoServicio) {
        this.tiempoServicio = tiempoServicio;
    }
}
