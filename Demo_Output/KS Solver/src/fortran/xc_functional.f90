! xc_functional.f90 - Exchange-Correlation Functional for DFT
! Implements LDA (Local Density Approximation) functionals

module xc_functional_module
    use grid_manager
    implicit none
    
    ! XC functional type
    integer, save :: xc_type  ! 1 = LDA, 2 = GGA
    
    ! XC energy and potential
    real(8), allocatable, save :: v_xc(:,:,:)    ! XC potential
    real(8), save :: xc_energy_total             ! Total XC energy
    
    ! Constants for LDA
    real(8), parameter :: PI = 3.14159265358979323846d0
    real(8), parameter :: RS_FACTOR = (3.0d0 / (4.0d0 * PI))**(1.0d0/3.0d0)
    
contains

    ! Initialize XC functional
    subroutine init_xc(xc_type_in, ierr)
        integer, intent(in) :: xc_type_in
        integer, intent(out) :: ierr
        
        xc_type = xc_type_in
        ierr = 0
        
        allocate(v_xc(nx, ny, nz), stat=ierr)
        if (ierr /= 0) then
            print *, 'Error: Failed to allocate XC arrays'
            return
        end if
        
        v_xc = 0.0d0
        xc_energy_total = 0.0d0
        
        print *, 'XC functional initialized: type=', xc_type
        
    end subroutine init_xc
    
    ! Compute XC potential and energy from density
    subroutine compute_xc(density, v_xc_out, exc_out)
        real(8), intent(in) :: density(:,:,:)
        real(8), intent(out) :: v_xc_out(:,:,:)
        real(8), intent(out) :: exc_out
        
        integer :: i, j, k
        real(8) :: rho, rs, v_x, v_c, e_x, e_c
        
        exc_out = 0.0d0
        
        do k = 1, nz
            do j = 1, ny
                do i = 1, nx
                    rho = density(i, j, k)
                    
                    if (rho > 1.0d-15) then
                        ! Calculate Wigner-Seitz radius
                        rs = RS_FACTOR / rho**(1.0d0/3.0d0)
                        
                        ! Exchange (Dirac exchange)
                        call lda_exchange(rho, rs, e_x, v_x)
                        
                        ! Correlation (Ceperley-Alder parameterization)
                        call lda_correlation(rs, e_c, v_c)
                        
                        ! Total XC potential and energy density
                        v_xc_out(i, j, k) = v_x + v_c
                        exc_out = exc_out + (e_x + e_c) * rho * dx * dy * dz
                    else
                        v_xc_out(i, j, k) = 0.0d0
                    end if
                end do
            end do
        end do
        
        v_xc = v_xc_out
        xc_energy_total = exc_out
        
    end subroutine compute_xc
    
    ! LDA exchange: Dirac exchange
    ! V_x = -3/4 * (3/pi)^(1/3) * rho^(1/3)
    subroutine lda_exchange(rho, rs, ex, vx)
        real(8), intent(in) :: rho, rs
        real(8), intent(out) :: ex, vx
        
        real(8) :: prefactor
        
        ! Prefactor: -3/4 * (3/pi)^(1/3)
        prefactor = -0.75d0 * (3.0d0 / PI)**(1.0d0/3.0d0)
        
        ! Exchange energy density
        ex = prefactor * rho**(1.0d0/3.0d0)
        
        ! Exchange potential (V_x = 4/3 * epsilon_x)
        vx = 4.0d0 / 3.0d0 * ex
        
    end subroutine lda_exchange
    
    ! LDA correlation: Ceperley-Alder parameterization
    subroutine lda_correlation(rs, ec, vc)
        real(8), intent(in) :: rs
        real(8), intent(out) :: ec, vc
        
        ! Parameters for Ceperley-Alder (unpolarized)
        real(8), parameter :: A = 0.0311d0
        real(8), parameter :: B = -0.048d0
        real(8), parameter :: C = 0.002d0
        real(8), parameter :: D = -0.0116d0
        real(8), parameter :: gamma = -0.1423d0
        real(8), parameter :: beta1 = 1.0529d0
        real(8), parameter :: beta2 = 0.3334d0
        
        real(8) :: ln_rs, sqrt_rs
        
        if (rs < 1.0d0) then
            ! High density limit
            ln_rs = log(rs)
            ec = A * ln_rs + B + C * rs * ln_rs + D * rs
            vc = ec - A/3.0d0 - C * rs / 3.0d0 * (ln_rs + 1.0d0) - D * rs / 3.0d0
        else
            ! Low density limit
            sqrt_rs = sqrt(rs)
            ec = gamma / (1.0d0 + beta1 * sqrt_rs + beta2 * rs)
            vc = ec * (1.0d0 + 7.0d0/6.0d0 * beta1 * sqrt_rs + &
                       4.0d0/3.0d0 * beta2 * rs) / &
                 (1.0d0 + beta1 * sqrt_rs + beta2 * rs)
        end if
        
    end subroutine lda_correlation
    
    ! Compute exchange only (for testing)
    subroutine compute_exchange_only(density, v_x_out, ex_out)
        real(8), intent(in) :: density(:,:,:)
        real(8), intent(out) :: v_x_out(:,:,:)
        real(8), intent(out) :: ex_out
        
        integer :: i, j, k
        real(8) :: rho, rs, e_x, v_x
        
        ex_out = 0.0d0
        
        do k = 1, nz
            do j = 1, ny
                do i = 1, nx
                    rho = density(i, j, k)
                    
                    if (rho > 1.0d-15) then
                        rs = RS_FACTOR / rho**(1.0d0/3.0d0)
                        call lda_exchange(rho, rs, e_x, v_x)
                        v_x_out(i, j, k) = v_x
                        ex_out = ex_out + e_x * rho * dx * dy * dz
                    else
                        v_x_out(i, j, k) = 0.0d0
                    end if
                end do
            end do
        end do
        
    end subroutine compute_exchange_only
    
    ! Get XC potential (for f2py)
    subroutine get_xc_potential(v_xc_out)
        real(8), intent(out) :: v_xc_out(nx, ny, nz)
        v_xc_out = v_xc
    end subroutine get_xc_potential
    
    ! Get XC energy
    function xc_energy() result(e_xc)
        real(8) :: e_xc
        e_xc = xc_energy_total
    end function xc_energy
    
    ! Clean up XC memory
    subroutine cleanup_xc()
        if (allocated(v_xc)) deallocate(v_xc)
        print *, 'XC functional memory cleaned up'
    end subroutine cleanup_xc
    
end module xc_functional_module