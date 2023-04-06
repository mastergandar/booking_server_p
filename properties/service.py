from rest_framework.exceptions import ValidationError

from properties.filters import PropertiesFilterSet


class PropertyService:

    @staticmethod
    def property_type_validation(attrs):
        if attrs['accommodation_type'] == 0:
            if 'house_type' not in attrs:
                raise ValidationError({'house_type': 'This field is required'})
            elif attrs['house_type'] is None:
                raise ValidationError({'house_type': 'Cannot be null'})
        elif attrs['accommodation_type'] == 1:
            if 'flat_type' not in attrs:
                raise ValidationError({'flat_type': 'This field is required'})
            elif attrs['flat_type'] is None:
                raise ValidationError({'flat_type': 'Cannot be null'})
        elif attrs['accommodation_type'] == 2:
            if 'room_type' not in attrs:
                raise ValidationError({'room_type': 'This field is required'})
            elif attrs['room_type'] is None:
                raise ValidationError({'room_type': 'Cannot be null'})
        elif attrs['accommodation_type'] == 3:
            if 'unique_type' not in attrs:
                raise ValidationError({'unique_type': 'This field is required'})
            elif attrs['unique_type'] is None:
                raise ValidationError({'unique_type': 'Cannot be null'})
        elif attrs['accommodation_type'] == 4:
            if 'hotel_type' not in attrs:
                raise ValidationError({'hotel_type': 'This field is required'})
            elif attrs['hotel_type'] is None:
                raise ValidationError({'hotel_type': 'Cannot be null'})

    def query_filter(self, queryset, accommodation_list, flat_list, house_list, room_list, unique_list, hotel_list,
                     rent_list, guests_count, bedrooms_count, bathrooms_count, beds_count):
        pf = PropertiesFilterSet()
        print(f"START QUERY: {queryset}")
        checks = [
            flat_list and hotel_list, flat_list and unique_list, flat_list and room_list, flat_list and house_list,
            house_list and hotel_list, house_list and unique_list, house_list and room_list, room_list and hotel_list,
            room_list and unique_list, unique_list and hotel_list
        ]
        lists = [accommodation_list, flat_list, house_list, room_list, unique_list, hotel_list, rent_list]
        if not any(lists):
            return queryset
        checked_lists = [[int(i) for i in lst.split(',')] if lst != '' else [] for lst in lists]
        print(f"CHECKED LISTS: {checked_lists}")
        if any(checks) is not None:
            combo_list = {
                'accommodation_list': checked_lists[0], 'flat_list': checked_lists[1], 'house_list': checked_lists[2],
                'room_list': checked_lists[3], 'unique_list': checked_lists[4], 'hotel_list': checked_lists[5],
                'rent_list': checked_lists[6], 'guests_count': guests_count, 'bedrooms_count': bedrooms_count,
                'bathrooms_count': bathrooms_count, 'beds_count': beds_count
            }
            if combo_list['guests_count'] == '':
                combo_list['guests_count'] = 0
            if combo_list['bedrooms_count'] == '':
                combo_list['bedrooms_count'] = 0
            if combo_list['bathrooms_count'] == '':
                combo_list['bathrooms_count'] = 0
            if combo_list['beds_count'] == '':
                combo_list['beds_count'] = 0
            print(f"COMBO LIST: {combo_list}")
            filtered_queryset = pf.combo_filter(queryset, '', combo_list)
            return filtered_queryset
        filtered_queryset = pf.filter_by_accommodation_type(queryset, '', accommodation_list)
        filtered_queryset = pf.filter_by_flat_type(filtered_queryset, '', flat_list)
        filtered_queryset = pf.filter_by_house_type(filtered_queryset, '', house_list)
        filtered_queryset = pf.filter_by_room_type(filtered_queryset, '', room_list)
        filtered_queryset = pf.filter_by_unique_type(filtered_queryset, '', unique_list)
        filtered_queryset = pf.filter_by_hotel_type(filtered_queryset, '', hotel_list)
        filtered_queryset = pf.filter_by_rent_type(filtered_queryset, '', rent_list)
        filtered_queryset = pf.filter_by_guests_count(filtered_queryset, 0, guests_count)
        filtered_queryset = pf.filter_by_bedrooms_count(filtered_queryset, 0, bedrooms_count)
        filtered_queryset = pf.filter_by_bathrooms_count(filtered_queryset, 0, bathrooms_count)
        filtered_queryset = pf.filter_by_beds_count(filtered_queryset, 0, beds_count)
        return filtered_queryset
