! poisson.f90 - Poisson Equation Solver for DFT
! Solves for Hartree potential: Laplacian(V_H) = -4*pi*rho

module poisson_module
    use grid_manager
    implicit none
    
    ! Hartree potential
    real(8), allocatable, save :: v_hartree(:,:,:)
    real(8), save :: hartree_energy
    
    ! Iterative solver parameters
    integer, save :: poisson_max_iter
    real(8), save :: poisson_tol
    
    ! Constants
    real(8), parameter :: PI = 3.14159265358979323846d0
    real(8), parameter :: FOUR_PI = 4.0d0 * PI
    
contains

    ! Initialize Poisson solver
    subroutine init_poisson(max_iter, tol, ierr)
        integer, intent(in) :: max_iter
        real(8), intent(in) :: tol
        integer, intent(out) :: ierr
        
        poisson_max_iter = max_iter
        poisson_tol = tol
        ierr = 0
        
        allocate(v_hartree(nx, ny, nz), stat=ierr)
        if (ierr /= 0) then
            print *, 'Error: Failed to allocate Hartree potential'
            return
        end if
        
        v_hartree = 0.0d0
        hartree_energy = 0.0d0
        
        print *, 'Poisson solver initialized: max_iter=', max_iter, ' tol=', tol
        
    end subroutine init_poisson
    
    ! Solve Poisson equation using iterative Gauss-Seidel method
    subroutine solve_poisson(density, converged, n_iter)
        real(8), intent(in) :: density(:,:,:)
        logical, intent(out) :: converged
        integer, intent(out) :: n_iter
        
        integer :: i, j, k, iter
        real(8) :: diff, max_diff, rhs
        real(8) :: v_new, dx2, dy2, dz2, denom
        
        converged = .false.
        dx2 = dx * dx
        dy2 = dy * dy
        dz2 = dz * dz
        denom = 2.0d0 * (1.0d0/dx2 + 1.0d0/dy2 + 1.0d0/dz2)
        
        ! Initial guess: zero potential
        v_hartree = 0.0d0
        
        ! Gauss-Seidel iteration
        do iter = 1, poisson_max_iter
            max_diff = 0.0d0
            
            do k = 2, nz-1
                do j = 2, ny-1
                    do i = 2, nx-1
                        ! Right-hand side: -4*pi*rho
                        rhs = -FOUR_PI * density(i, j, k)
                        
                        ! Gauss-Seidel update
                        v_new = ((v_hartree(i+1,j,k) + v_hartree(i-1,j,k)) / dx2 + &
                                 (v_hartree(i,j+1,k) + v_hartree(i,j-1,k)) / dy2 + &
                                 (v_hartree(i,j,k+1) + v_hartree(i,j,k-1)) / dz2 - rhs) / denom
                        
                        ! Track maximum change
                        diff = abs(v_new - v_hartree(i, j, k))
                        if (diff > max_diff) max_diff = diff
                        
                        ! Update potential
                        v_hartree(i, j, k) = v_new
                    end do
                end do
            end do
            
            ! Apply boundary conditions (zero at boundaries)
            v_hartree(1,:,:) = 0.0d0
            v_hartree(nx,:,:) = 0.0d0
            v_hartree(:,1,:) = 0.0d0
            v_hartree(:,ny,:) = 0.0d0
            v_hartree(:,:,1) = 0.0d0
            v_hartree(:,:,nz) = 0.0d0
            
            ! Check convergence
            if (max_diff < poisson_tol) then
                converged = .true.
                n_iter = iter
                print *, 'Poisson solver converged in ', iter, ' iterations'
                exit
            end if
        end do
        
        if (.not. converged) then
            n_iter = poisson_max_iter
            print *, 'Poisson solver did not converge, max_diff=', max_diff
        end if
        
        ! Calculate Hartree energy
        hartree_energy = 0.5d0 * sum(density * v_hartree) * dx * dy * dz
        
    end subroutine solve_poisson
    
    ! Solve using Successive Over-Relaxation (SOR) - faster convergence
    subroutine solve_poisson_sor(density, omega, converged, n_iter)
        real(8), intent(in) :: density(:,:,:)
        real(8), intent(in) :: omega      ! Relaxation parameter (1 < omega < 2)
        logical, intent(out) :: converged
        integer, intent(out) :: n_iter
        
        integer :: i, j, k, iter
        real(8) :: diff, max_diff, rhs, v_old, v_new
        real(8) :: dx2, dy2, dz2, denom
        
        converged = .false.
        dx2 = dx * dx
        dy2 = dy * dy
        dz2 = dz * dz
        denom = 2.0d0 * (1.0d0/dx2 + 1.0d0/dy2 + 1.0d0/dz2)
        
        v_hartree = 0.0d0
        
        do iter = 1, poisson_max_iter
            max_diff = 0.0d0
            
            do k = 2, nz-1
                do j = 2, ny-1
                    do i = 2, nx-1
                        rhs = -FOUR_PI * density(i, j, k)
                        v_old = v_hartree(i, j, k)
                        
                        ! SOR update
                        v_new = ((v_hartree(i+1,j,k) + v_hartree(i-1,j,k)) / dx2 + &
                                 (v_hartree(i,j+1,k) + v_hartree(i,j-1,k)) / dy2 + &
                                 (v_hartree(i,j,k+1) + v_hartree(i,j,k-1)) / dz2 - rhs) / denom
                        
                        v_hartree(i, j, k) = v_old + omega * (v_new - v_old)
                        
                        diff = abs(v_hartree(i, j, k) - v_old)
                        if (diff > max_diff) max_diff = diff
                    end do
                end do
            end do
            
            ! Boundary conditions
            v_hartree(1,:,:) = 0.0d0
            v_hartree(nx,:,:) = 0.0d0
            v_hartree(:,1,:) = 0.0d0
            v_hartree(:,ny,:) = 0.0d0
            v_hartree(:,:,1) = 0.0d0
            v_hartree(:,:,nz) = 0.0d0
            
            if (max_diff < poisson_tol) then
                converged = .true.
                n_iter = iter
                print *, 'Poisson SOR converged in ', iter, ' iterations'
                exit
            end if
        end do
        
        if (.not. converged) then
            n_iter = poisson_max_iter
        end if
        
        hartree_energy = 0.5d0 * sum(density * v_hartree) * dx * dy * dz
        
    end subroutine solve_poisson_sor
    
    ! Get Hartree potential (for f2py)
    subroutine get_hartree_potential(v_h_out)
        real(8), intent(out) :: v_h_out(nx, ny, nz)
        v_h_out = v_hartree
    end subroutine get_hartree_potential
    
    ! Get Hartree energy
    function get_hartree_energy() result(e_h)
        real(8) :: e_h
        e_h = hartree_energy
    end function get_hartree_energy
    
    ! Clean up Poisson memory
    subroutine cleanup_poisson()
        if (allocated(v_hartree)) deallocate(v_hartree)
        print *, 'Poisson solver memory cleaned up'
    end subroutine cleanup_poisson
    
end module poisson_module