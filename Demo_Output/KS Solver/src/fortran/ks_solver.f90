! ks_solver.f90 - Kohn-Sham Equation Solver for DFT
! Solves the KS equations using finite difference discretization

module ks_solver_module
    use grid_manager
    implicit none
    
    ! Number of occupied states
    integer, save :: nstates
    
    ! Wavefunctions and eigenvalues
    real(8), allocatable, save :: psi(:,:,:,:)    ! Wavefunctions (nx,ny,nz,nstate)
    real(8), allocatable, save :: eigenvalues(:)  ! Orbital energies
    
contains

    ! Initialize KS solver with number of states
    subroutine init_ks_solver(nstates_in, ierr)
        integer, intent(in) :: nstates_in
        integer, intent(out) :: ierr
        
        nstates = nstates_in
        ierr = 0
        
        ! Allocate wavefunction array
        allocate(psi(nx, ny, nz, nstates), stat=ierr)
        if (ierr /= 0) then
            print *, 'Error: Failed to allocate wavefunctions'
            return
        end if
        
        ! Allocate eigenvalues
        allocate(eigenvalues(nstates), stat=ierr)
        if (ierr /= 0) then
            print *, 'Error: Failed to allocate eigenvalues'
            return
        end if
        
        ! Initialize to zero
        psi = 0.0d0
        eigenvalues = 0.0d0
        
        print *, 'KS solver initialized for ', nstates, ' states'
        
    end subroutine init_ks_solver
    
    ! Solve Kohn-Sham equations for given potential
    ! Uses finite difference for kinetic energy + potential
    subroutine solve_ks(potential, niter_max, tol, converged)
        real(8), intent(in) :: potential(:,:,:)    ! Effective potential
        integer, intent(in) :: niter_max           ! Max iterations
        real(8), intent(in) :: tol                 ! Convergence tolerance
        logical, intent(out) :: converged
        
        ! Local variables
        integer :: i, j, k, n, iter
        real(8) :: kinetic_prefactor
        real(8) :: energy_old, energy_new, diff
        real(8), allocatable :: psi_new(:,:,:)
        
        allocate(psi_new(nx, ny, nz))
        kinetic_prefactor = -0.5d0  ! hbar^2/(2m) in atomic units
        
        converged = .false.
        
        ! Initialize wavefunctions with random guess
        call random_number(psi)
        
        ! Simple power iteration for ground state
        do iter = 1, niter_max
            energy_old = sum(eigenvalues)
            
            ! Update each state
            do n = 1, nstates
                call apply_hamiltonian(psi(:,:,:,n), psi_new, potential, kinetic_prefactor)
                
                ! Normalize
                call normalize_wavefunction(psi_new)
                
                ! Update psi
                psi(:,:,:,n) = psi_new
                
                ! Calculate eigenvalue (expectation value of H)
                call calculate_eigenvalue(psi(:,:,:,n), potential, eigenvalues(n))
            end do
            
            energy_new = sum(eigenvalues)
            diff = abs(energy_new - energy_old)
            
            if (diff < tol) then
                converged = .true.
                print *, 'KS solver converged in ', iter, ' iterations'
                exit
            end if
        end do
        
        if (.not. converged) then
            print *, 'KS solver did not converge after ', niter_max, ' iterations'
        end if
        
        deallocate(psi_new)
        
    end subroutine solve_ks
    
    ! Apply Hamiltonian operator to wavefunction
    ! H = T + V = -1/2 * Laplacian + V
    subroutine apply_hamiltonian(psi_in, psi_out, potential, kinetic_coeff)
        real(8), intent(in) :: psi_in(:,:,:)
        real(8), intent(out) :: psi_out(:,:,:)
        real(8), intent(in) :: potential(:,:,:)
        real(8), intent(in) :: kinetic_coeff
        
        integer :: i, j, k
        real(8) :: laplacian
        
        ! Apply kinetic energy (finite difference Laplacian)
        do k = 2, nz-1
            do j = 2, ny-1
                do i = 2, nx-1
                    ! 7-point stencil for Laplacian
                    laplacian = (psi_in(i+1,j,k) + psi_in(i-1,j,k)) / (dx*dx) + &
                               (psi_in(i,j+1,k) + psi_in(i,j-1,k)) / (dy*dy) + &
                               (psi_in(i,j,k+1) + psi_in(i,j,k-1)) / (dz*dz) - &
                               2.0d0 * psi_in(i,j,k) * (1.0d0/(dx*dx) + 1.0d0/(dy*dy) + 1.0d0/(dz*dz))
                    
                    psi_out(i,j,k) = kinetic_coeff * laplacian + potential(i,j,k) * psi_in(i,j,k)
                end do
            end do
        end do
        
        ! Boundary conditions (zero)
        psi_out(1,:,:) = 0.0d0
        psi_out(nx,:,:) = 0.0d0
        psi_out(:,1,:) = 0.0d0
        psi_out(:,ny,:) = 0.0d0
        psi_out(:,:,1) = 0.0d0
        psi_out(:,:,nz) = 0.0d0
        
    end subroutine apply_hamiltonian
    
    ! Normalize wavefunction
    subroutine normalize_wavefunction(wfn)
        real(8), intent(inout) :: wfn(:,:,:)
        real(8) :: norm
        
        norm = sum(wfn * wfn) * dx * dy * dz
        if (norm > 1.0d-15) then
            wfn = wfn / sqrt(norm)
        end if
        
    end subroutine normalize_wavefunction
    
    ! Calculate eigenvalue as expectation value of Hamiltonian
    subroutine calculate_eigenvalue(wfn, potential, eval)
        real(8), intent(in) :: wfn(:,:,:)
        real(8), intent(in) :: potential(:,:,:)
        real(8), intent(out) :: eval
        
        real(8), allocatable :: h_psi(:,:,:)
        real(8) :: kinetic_coeff
        
        allocate(h_psi(nx, ny, nz))
        kinetic_coeff = -0.5d0
        
        call apply_hamiltonian(wfn, h_psi, potential, kinetic_coeff)
        
        ! <psi|H|psi>
        eval = sum(wfn * h_psi) * dx * dy * dz
        
        deallocate(h_psi)
        
    end subroutine calculate_eigenvalue
    
    ! Get wavefunctions (for f2py)
    subroutine get_wavefunctions(psi_out, nstates_out)
        real(8), intent(out) :: psi_out(nx, ny, nz, nstates)
        integer, intent(out) :: nstates_out
        
        psi_out = psi
        nstates_out = nstates
        
    end subroutine get_wavefunctions
    
    ! Get eigenvalues (for f2py)
    subroutine get_eigenvalues(eval_out, nstates_out)
        real(8), intent(out) :: eval_out(nstates)
        integer, intent(out) :: nstates_out
        
        eval_out = eigenvalues
        nstates_out = nstates
        
    end subroutine get_eigenvalues
    
    ! Clean up KS solver memory
    subroutine cleanup_ks_solver()
        if (allocated(psi)) deallocate(psi)
        if (allocated(eigenvalues)) deallocate(eigenvalues)
        print *, 'KS solver memory cleaned up'
    end subroutine cleanup_ks_solver
    
end module ks_solver_module