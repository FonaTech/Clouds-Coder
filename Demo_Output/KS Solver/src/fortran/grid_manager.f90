! grid_manager.f90 - 3D Real-Space Grid Management for DFT
! Provides grid initialization, memory allocation, and grid operations

module grid_manager
    implicit none
    
    ! Grid parameters
    integer, save :: nx, ny, nz           ! Grid points in each dimension
    real(8), save :: dx, dy, dz           ! Grid spacing
    real(8), save :: Lx, Ly, Lz           ! Box dimensions
    integer, save :: ntotal               ! Total grid points
    
    ! Grid arrays
    real(8), allocatable, save :: x(:)    ! x-coordinates
    real(8), allocatable, save :: y(:)    ! y-coordinates
    real(8), allocatable, save :: z(:)    ! z-coordinates
    
contains

    ! Initialize the 3D grid with given parameters
    subroutine init_grid(nx_in, ny_in, nz_in, Lx_in, Ly_in, Lz_in)
        integer, intent(in) :: nx_in, ny_in, nz_in
        real(8), intent(in) :: Lx_in, Ly_in, Lz_in
        integer :: i, ierr
        
        ! Set grid dimensions
        nx = nx_in
        ny = ny_in
        nz = nz_in
        Lx = Lx_in
        Ly = Ly_in
        Lz = Lz_in
        
        ! Calculate grid spacing
        dx = Lx / dble(nx)
        dy = Ly / dble(ny)
        dz = Lz / dble(nz)
        
        ! Total grid points
        ntotal = nx * ny * nz
        
        ! Allocate coordinate arrays
        allocate(x(nx), y(ny), z(nz), stat=ierr)
        if (ierr /= 0) then
            print *, 'Error: Failed to allocate grid arrays'
            stop 1
        end if
        
        ! Generate coordinate grids
        do i = 1, nx
            x(i) = (dble(i) - 0.5d0) * dx - Lx/2.0d0
        end do
        
        do i = 1, ny
            y(i) = (dble(i) - 0.5d0) * dy - Ly/2.0d0
        end do
        
        do i = 1, nz
            z(i) = (dble(i) - 0.5d0) * dz - Lz/2.0d0
        end do
        
        print *, 'Grid initialized: ', nx, 'x', ny, 'x', nz, ' = ', ntotal, ' points'
        print *, 'Grid spacing: dx=', dx, ' dy=', dy, ' dz=', dz
        
    end subroutine init_grid
    
    ! Allocate a 3D scalar field
    subroutine allocate_scalar_field(field, ierr)
        real(8), allocatable, intent(out) :: field(:,:,:)
        integer, intent(out) :: ierr
        
        allocate(field(nx, ny, nz), stat=ierr)
        if (ierr /= 0) then
            print *, 'Error: Failed to allocate scalar field'
        else
            field = 0.0d0
        end if
        
    end subroutine allocate_scalar_field
    
    ! Deallocate a 3D scalar field
    subroutine deallocate_scalar_field(field)
        real(8), allocatable, intent(inout) :: field(:,:,:)
        
        if (allocated(field)) then
            deallocate(field)
        end if
        
    end subroutine deallocate_scalar_field
    
    ! Get grid info (for f2py interface)
    subroutine get_grid_info(nx_out, ny_out, nz_out, dx_out, dy_out, dz_out, ntotal_out)
        integer, intent(out) :: nx_out, ny_out, nz_out, ntotal_out
        real(8), intent(out) :: dx_out, dy_out, dz_out
        
        nx_out = nx
        ny_out = ny
        nz_out = nz
        dx_out = dx
        dy_out = dy
        dz_out = dz
        ntotal_out = ntotal
        
    end subroutine get_grid_info
    
    ! Clean up grid memory
    subroutine cleanup_grid()
        if (allocated(x)) deallocate(x)
        if (allocated(y)) deallocate(y)
        if (allocated(z)) deallocate(z)
        print *, 'Grid memory cleaned up'
    end subroutine cleanup_grid
    
end module grid_manager