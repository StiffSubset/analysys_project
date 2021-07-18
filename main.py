from geo_module import GeoModule

gm = GeoModule()

gm.easy_capital_test()
gm.hard_capital_test()
gm.country_test(area=False)

print(gm.country_info('Иордания'), '\n')
print(gm.get_info(['Азия', 'Америка', 'Африка'], max_area_value=10000, min_population_value=1000000))
