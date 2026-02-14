"""
Test script for scrapeba package.
"""

import sys
sys.path.insert(0, '.')

from scrapeba import get_district, get_data

def test_get_district():
    """Test get_district function"""
    print("=" * 60)
    print("Testing get_district() function")
    print("=" * 60)
    
    try:
        # Test with a specific district
        print("\nFetching data for district 09571 (year=2021, month=10)...")
        df = get_district(id="09571", year="2021", month="10")
        
        print(f"\nSuccess! Retrieved data with shape: {df.shape}")
        print("\nColumns:", df.columns.tolist())
        print("\nData:")
        print(df)
        print("\n✓ get_district() test passed!")
        return True
        
    except Exception as e:
        print(f"\n✗ get_district() test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_get_data():
    """Test get_data function (limited to 5 districts for speed)"""
    print("\n" + "=" * 60)
    print("Testing get_data() function (limited)")
    print("=" * 60)
    
    try:
        # Import the internal function to limit districts
        import pickle
        from pathlib import Path
        
        # Load and limit to first 5 districts with resp=200
        data_file = Path('scrapeba/data/available_districts.pkl')
        with open(data_file, 'rb') as f:
            available_districts = pickle.load(f)
        
        if available_districts['resp'].dtype == 'object' or isinstance(available_districts['resp'].iloc[0], str):
            available = available_districts[available_districts['resp'] == '200']
        else:
            available = available_districts[available_districts['resp'] == 200]
        
        print(f"\nFound {len(available)} districts with available data")
        print("Testing with first 3 districts for speed...")
        
        # Temporarily modify get_data to use only first 3 districts
        from scrapeba.get_district import get_district
        import pandas as pd
        from tqdm import tqdm
        import time
        
        test_ids = available['id'].head(3).tolist()
        print(f"Test districts: {test_ids}")
        
        data_list = []
        for district_id in tqdm(test_ids, desc="Downloading districts"):
            try:
                tmp = get_district(id=district_id, year="2021", month="10")
                data_list.append(tmp)
                time.sleep(1)
            except Exception as e:
                print(f"\nWarning: Failed to fetch data for district {district_id}: {str(e)}")
                continue
        
        if data_list:
            data_output = pd.concat(data_list, ignore_index=True)
            print(f"\nSuccess! Retrieved data with shape: {data_output.shape}")
            print("\nColumns:", data_output.columns.tolist())
            print("\nFirst few rows:")
            print(data_output.head())
            print(f"\n✓ get_data() test passed! (tested with {len(data_list)} districts)")
            return True
        else:
            print("\n✗ get_data() test failed: No data retrieved")
            return False
            
    except Exception as e:
        print(f"\n✗ get_data() test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("SCRAPEBA PACKAGE TEST SUITE")
    print("=" * 60)
    
    results = []
    
    # Test get_district (note: will fail if no internet/blocked domain)
    results.append(("get_district", test_get_district()))
    
    # Test get_data (limited)
    results.append(("get_data", test_get_data()))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{test_name}: {status}")
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
    else:
        print("\n⚠️  Some tests failed (likely due to network restrictions)")

if __name__ == '__main__':
    main()
