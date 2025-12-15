import math

# Vector operations for Python 3.3 (No numpy)
# Vectors are assumed to be tuples/lists of 3 floats (x, y, z)

def vec_sub(a, b):
    """Returns vector a - b"""
    return (a[0]-b[0], a[1]-b[1], a[2]-b[2])

def vec_add(a, b):
    """Returns vector a + b"""
    return (a[0]+b[0], a[1]+b[1], a[2]+b[2])

def vec_dot(a, b):
    """Dot product of a and b"""
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

def vec_mag_sq(a):
    """Magnitude squared"""
    return a[0]*a[0] + a[1]*a[1] + a[2]*a[2]

def vec_dist_sq(a, b):
    """Distance squared between two points"""
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    dz = a[2] - b[2]
    return dx*dx + dy*dy + dz*dz

def project_point_on_line_segment(p, a, b):
    """
    Finds the closest point on segment AB to point P.
    Returns (closest_point_xyz, t_factor)
    """
    ap = vec_sub(p, a)
    ab = vec_sub(b, a)
    ab_len_sq = vec_mag_sq(ab)
    
    if ab_len_sq < 0.000001:
        return a, 0.0

    t = vec_dot(ap, ab) / ab_len_sq
    
    # Clamp to segment
    t_clamped = max(0.0, min(1.0, t))
    
    closest = (
        a[0] + ab[0]*t_clamped,
        a[1] + ab[1]*t_clamped,
        a[2] + ab[2]*t_clamped
    )
    return closest, t_clamped

def is_point_in_cylinder(p, line_a, line_b, radius):
    """
    Checks if point p is within 'radius' distance of the line segment ab.
    Used for virtual beam detection.
    """
    closest, t = project_point_on_line_segment(p, line_a, line_b)
    dist_sq = vec_dist_sq(p, closest)
    return dist_sq <= (radius * radius)
