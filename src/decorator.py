from error import EmptyBaitException, UnimplementedException, NoEnergyException
from utils import go_main_screen as do_go_main_screen
from datetime import datetime
from debug import save_print_dbg
from const import TIME_FORMAT
import const


def unimplemented(f):
    def wrapper(*args, **kwargs):
        print(UnimplementedException(kwargs['feature']).__str__())
        return
    return wrapper


def feature(feature: str):
    def decorator(f):
        def wrapper(*args, **kwargs):
            kwargs['feature'] = feature
            rename = feature.replace(' ', '_')
            const.dbg_name = datetime.now().strftime(f'{TIME_FORMAT}_{rename}')
            save_print_dbg(f"\n***Debug for '{const.dbg_name}'***")
            result = f(*args, **kwargs)
            save_print_dbg(f"***Finished '{const.dbg_name}***'")
            return result
        return wrapper
    return decorator


def go_main_screen(f):
    def wrapper(*args, **kwargs):
        do_go_main_screen()
        return f(*args, **kwargs)
    return wrapper


def farm_exceptions(f):
    def wrapper(*args, **kwargs):
        err = ''
        try:
            return f(*args, **kwargs)
        except NoEnergyException:
            err = NoEnergyException(feature=kwargs['feature']).__str__()
        except KeyboardInterrupt:
            err = f"'{kwargs['feature']}' stopped by keyboard".__str__()
        except EmptyBaitException as ex:
            err = ex.__str__()
        except Exception as ex:
            err = f"got error when run '{kwargs['feature']}': {ex.__str__()}"
        print(err)
        save_print_dbg(txt=err, is_print=False)
    return wrapper
