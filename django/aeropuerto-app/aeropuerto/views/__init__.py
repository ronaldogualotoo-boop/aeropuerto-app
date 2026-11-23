from .aeronave_views import (
    aeronave_create,
    aeronave_delete,
    aeronave_detail,
    aeronave_list,
    aeronave_update,
)
from .aerolinea_views import (
    aerolinea_create,
    aerolinea_delete,
    aerolinea_detail,
    aerolinea_list,
    aerolinea_update,
)
from .aeropuerto_views import (
    aeropuerto_create,
    aeropuerto_delete,
    aeropuerto_detail,
    aeropuerto_list,
    aeropuerto_update,
)
from .auth_views import login_view, logout_view, registro
from .home_views import home
from .vuelo_views import vuelo_create, vuelo_delete, vuelo_detail, vuelo_list, vuelo_update

__all__ = [name for name in globals() if not name.startswith("_")]
