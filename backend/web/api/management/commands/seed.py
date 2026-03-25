import json
import csv
from django.core.management.base import BaseCommand
from api.models import Supplier, Bolt, Test, TestCurve
from pathlib import Path


class Command(BaseCommand):
    help = 'Seed the database with bolt test data from JSON and CSV files'

    def add_arguments(self, parser):
        parser.add_argument(
            '--flush',
            action='store_true',
            help='Clear all existing data before seeding'
        )

    def handle(self, *args, **options):
        # Clear existing data if --flush flag is provided
        if options['flush']:
            self.stdout.write(self.style.WARNING("Clearing existing data..."))
            TestCurve.objects.all().delete()
            Test.objects.all().delete()
            Bolt.objects.all().delete()
            Supplier.objects.all().delete()
        
        # Load products
        products_file = Path(__file__).resolve().parent.parent.parent / 'mock_data' / 'products.json'
        with open(products_file, 'r') as f:
            products = json.load(f)
        
        # Create supplier
        self.stdout.write(self.style.SUCCESS("Creating supplier..."))
        supplier = Supplier.objects.create(name="Supplier A")
        
        # Create bolts and map by name
        self.stdout.write(self.style.SUCCESS("Creating bolts..."))
        bolt_map = {}
        for product in products:
            bolt = Bolt.objects.create(
                supplier=supplier,
                name=product['product_name'],
                length=float(product['bolt_length']),
                diameter=float(product['bolt_diameter']),
                category=product['bolt_category'],
                equipment_compatibility=product['equipment_compatibility'],
                is_published=True
            )
            bolt_map[product['product_name']] = bolt
        
        # Load tests
        tests_file = Path(__file__).resolve().parent.parent.parent / 'mock_data' / 'tests.json'
        with open(tests_file, 'r') as f:
            tests_data = json.load(f)
        
        # Build test-to-bolt mapping from test_curves.csv
        curves_file = Path(__file__).resolve().parent.parent.parent / 'mock_data' / 'test_curves.csv'
        test_to_bolt_map = {}
        curve_data_by_test = {}
        
        with open(curves_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            # Strip whitespace from fieldnames
            reader.fieldnames = [field.strip() if field else field for field in reader.fieldnames]
            
            for row in reader:
                # Skip empty rows
                if not row or all(not v for v in row.values()):
                    continue
                
                # Create a clean row dict with stripped keys and values
                clean_row = {k.strip() if k else k: v.strip() if v else v for k, v in row.items()}
                
                test_id = int(clean_row['TestID'])
                product_name = clean_row['Product Name']
                
                # Map test to bolt
                if test_id not in test_to_bolt_map:
                    test_to_bolt_map[test_id] = product_name
                
                # Collect curve data (convert empty strings to None)
                if test_id not in curve_data_by_test:
                    curve_data_by_test[test_id] = []
                
                displacement_str = clean_row.get('Displacement (mm)', '').strip()
                load_str = clean_row.get('Dynamic Load (kN)', '').strip()
                
                curve_data_by_test[test_id].append({
                    'displacement': float(displacement_str) if displacement_str else None,
                    'load': float(load_str) if load_str else None
                })
        
        # Create tests
        self.stdout.write(self.style.SUCCESS("Creating tests..."))
        test_map = {}
        for test_data in tests_data:
            test_id = int(test_data['test_id'])
            
            # Determine which bolt this test belongs to
            if test_id in test_to_bolt_map:
                # Use mapping from curves CSV
                bolt_name = test_to_bolt_map[test_id]
                bolt = bolt_map.get(bolt_name)
            else:
                # If no explicit mapping, assign to first bolt
                bolt = list(bolt_map.values())[0]
            
            if bolt:
                test = Test.objects.create(
                    bolt=bolt,
                    methodology=test_data['test_methodology'],
                    facility=test_data['test_facility'],
                    installation_method=test_data.get('installation_method'),
                    encapsulation_method=test_data.get('encapsulation_method'),
                    peak_strength=test_data.get('peak_strength'),
                    bond_strength=test_data.get('bond_strength'),
                    yield_strength=test_data.get('yield_strength'),
                    ultimate_deformation=test_data.get('ultimate_deformation'),
                    stiffness=test_data.get('stiffness'),
                    loading_rate=test_data.get('loading_rate'),
                    energy_absorption=test_data.get('energy_absorption'),
                    number_of_drops=test_data.get('number_of_drops'),
                    is_published=True
                )
                test_map[test_id] = test
        
        # Create TestCurve objects
        self.stdout.write(self.style.SUCCESS("Creating test curves..."))
        for test_id, curve_pairs in curve_data_by_test.items():
            if test_id in test_map:
                TestCurve.objects.create(
                    test=test_map[test_id],
                    curve_pair=curve_pairs,
                    is_published=True
                )
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded database'))
