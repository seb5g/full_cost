from .utils.file_management import get_all_activities


def get_all_activity(request):
    all_activity_short, all_activity_long = get_all_activities()
    return {'all_activity_short': all_activity_short, 'all_activity_long': all_activity_long,}

