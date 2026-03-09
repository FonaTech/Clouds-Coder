! scf_loop.f90 - Self-Consistent Field Loop for DFT
! Manages SCF iterations, density mixing, and convergence

module scf_loop_module
    use grid_manager
    use ks_solver_module
    implicit none
    
    ! SCF parameters
    integer, save :: scf_max_iter      ! Maximum SCF iterations
    real(8), save :: energy_tol        ! Energy convergence tolerance
    real(8), save :: density_tol       ! Density convergence tolerance
    real(8), save :: mixing_alpha      ! Mixing parameter (0 < alpha < 1)
    
    ! SCF state
    real(8), allocatable, save :: density(:,:,:)       ! Electron density
    real(8), allocatable, save :: density_old(:,:,:)   ! Previous density
    real(8), allocatable, save :: v_eff(:,:,:)         ! Effective potential
    real(8), allocatable, save :: v_hartree(:,:,:)     ! Hartree potential
    real(8), allocatable, save :: v_xc(:,:,:)          ! XC potential
    
    ! Convergence history
    integer, save :: scf_iter_count
    real(8), allocatable, save :: energy_history(:)
    real(8), allocatable, save :: density_diff_history(:)
    
contains

    ! Initialize SCF loop
    subroutine init_scf(max_iter, e_tol, d_tol, alpha, ierr)
        integer, intent(in) :: max_iter
        real(8), intent(in) :: e_tol, d_tol, alpha
        integer, intent(out) :: ierr
        
        scf_max_iter = max_iter
        energy_tol = e_tol
        density_tol = d_tol
        mixing_alpha = alpha
        ierr = 0
        
        ! Allocate arrays
        allocate(density(nx, ny, nz), stat=ierr)
        allocate(density_old(nx, ny, nz), stat=ierr)
        allocate(v_eff(nx, ny, nz), stat=ierr)
        allocate(v_hartree(nx, ny, nz), stat=ierr)
        allocate(v_xc(nx, ny, nz), stat=ierr)
        allocate(energy_history(max_iter), stat=ierr)
        allocate(density_diff_history(max_iter), stat=ierr)
        
        if (ierr /= 0) then
            print *, 'Error: Failed to allocate SCF arrays'
            return
        end if
        
        ! Initialize to zero
        density = 0.0d0
        density_old = 0.0d0
        v_eff = 0.0d0
        v_hartree = 0.0d0
        v_xc = 0.0d0
        energy_history = 0.0d0
        density_diff_history = 0.0d0
        scf_iter_count = 0
        
        print *, 'SCF loop initialized: max_iter=', max_iter, ' energy_tol=', e_tol
        
    end subroutine init_scf
    
    ! Compute electron density from wavefunctions
    subroutine compute_density()
        integer :: i, j, k, n
        real(8) :: occ
        
        density = 0.0d0
        
        ! Sum |psi|^2 for each occupied state
        ! Assuming 2 electrons per orbital (spin-paired)
        do n = 1, nstates
            occ = 2.0d0  ! Occupation number
            do k = 1, nz
                do j = 1, ny
                    do i = 1, nx
                        density(i,j,k) = density(i,j,k) + occ * psi(i,j,k,n) * psi(i,j,k,n)
                    end do
                end do
            end do
        end do
        
    end subroutine compute_density
    
    ! Mix old and new densities (simple linear mixing)
    subroutine mix_density()
        real(8) :: diff
        
        ! Calculate density difference
        diff = sqrt(sum((density - density_old)**2) * dx * dy * dz)
        
        ! Linear mixing: rho_new = alpha * rho_new + (1-alpha) * rho_old
        density = mixing_alpha * density + (1.0d0 - mixing_alpha) * density_old
        
        ! Store for history
        scf_iter_count = scf_iter_count + 1
        density_diff_history(scf_iter_count) = diff
        
        print *, 'SCF iteration ', scf_iter_count, ' density diff = ', diff
        
    end subroutine mix_density
    
    ! Check SCF convergence
    subroutine check_convergence(converged, energy_diff, density_diff)
        logical, intent(out) :: converged
        real(8), intent(out) :: energy_diff, density_diff
        
        real(8) :: total_energy
        
        ! Calculate total energy
        call calculate_total_energy(total_energy)
        energy_history(scf_iter_count) = total_energy
        
        ! Get density difference
        density_diff = density_diff_history(scf_iter_count)
        
        ! Calculate energy difference
        if (scf_iter_count > 1) then
            energy_diff = abs(energy_history(scf_iter_count) - energy_history(scf_iter_count-1))
        else
            energy_diff = abs(energy_history(scf_iter_count))
        end if
        
        ! Check convergence
        if (energy_diff < energy_tol .and. density_diff < density_tol) then
            converged = .true.
            print *, 'SCF CONVERGED!'
            print *, '  Energy difference: ', energy_diff
            print *, '  Density difference: ', density_diff
        else
            converged = .false.
        end if
        
    end subroutine check_convergence
    
    ! Calculate total energy
    subroutine calculate_total_energy(total_energy)
        real(8), intent(out) :: total_energy
        
        real(8) :: kinetic_energy, hartree_energy, xc_energy
        
        ! Kinetic energy from eigenvalues
        kinetic_energy = sum(eigenvalues(1:nstates)) * 2.0d0  ! Factor of 2 for spin
        
        ! Hartree energy: 0.5 * integral(rho * V_H)
        hartree_energy = 0.5d0 * sum(density * v_hartree) * dx * dy * dz
        
        ! XC energy (approximate)
        xc_energy = sum(density * v_xc) * dx * dy * dz
        
        total_energy = kinetic_energy - hartree_energy + xc_energy
        
    end subroutine calculate_total_energy
    
    ! Update effective potential
    subroutine update_effective_potential(v_ext)
        real(8), intent(in) :: v_ext(:,:,:)  ! External potential
        
        ! V_eff = V_ext + V_Hartree + V_XC
        v_eff = v_ext + v_hartree + v_xc
        
    end subroutine update_effective_potential
    
    ! Run full SCF loop
    subroutine run_scf(v_ext, converged, n_iter)
        real(8), intent(in) :: v_ext(:,:,:)
        logical, intent(out) :: converged
        integer, intent(out) :: n_iter
        
        logical :: ks_converged
        real(8) :: energy_diff, density_diff
        integer :: iter
        
        converged = .false.
        
        ! Initial density guess
        call compute_density()
        density_old = density
        
        do iter = 1, scf_max_iter
            ! Update potentials
            call update_effective_potential(v_ext)
            
            ! Solve KS equations
            call solve_ks(v_eff, 100, 1.0d-6, ks_converged)
            
            ! Compute new density
            density_old = density
            call compute_density()
            
            ! Mix densities
            call mix_density()
            
            ! Check convergence
            call check_convergence(converged, energy_diff, density_diff)
            
            if (converged) exit
        end do
        
        n_iter = min(iter, scf_max_iter)
        
        if (.not. converged) then
            print *, 'SCF did not converge after ', n_iter, ' iterations'
        end if
        
    end subroutine run_scf
    
    ! Get density (for f2py)
    subroutine get_density(rho_out)
        real(8), intent(out) :: rho_out(nx, ny, nz)
        rho_out = density
    end subroutine get_density
    
    ! Get SCF history (for f2py)
    subroutine get_scf_history(n_iter, e_hist, d_hist)
        integer, intent(out) :: n_iter
        real(8), intent(out) :: e_hist(scf_max_iter), d_hist(scf_max_iter)
        
        n_iter = scf_iter_count
        e_hist = energy_history
        d_hist = density_diff_history
        
    end subroutine get_scf_history
    
    ! Clean up SCF memory
    subroutine cleanup_scf()
        if (allocated(density)) deallocate(density)
        if (allocated(density_old)) deallocate(density_old)
        if (allocated(v_eff)) deallocate(v_eff)
        if (allocated(v_hartree)) deallocate(v_hartree)
        if (allocated(v_xc)) deallocate(v_xc)
        if (allocated(energy_history)) deallocate(energy_history)
        if (allocated(density_diff_history)) deallocate(density_diff_history)
        print *, 'SCF memory cleaned up'
    end subroutine cleanup_scf
    
end module scf_loop_module