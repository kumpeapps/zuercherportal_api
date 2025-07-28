#!/usr/bin/env python3
"""
Performance Testing Script for zuercherportal_api
Tests multiple API calls to measure performance improvements
"""

import time
import statistics
import zuercherportal_api as zuercherportal


def measure_api_performance(jail, num_calls=5, records_per_page=10):
    """Measure API performance over multiple calls"""
    print(f"\n🔍 Testing {jail.name}")
    print(f"📊 Running {num_calls} API calls with {records_per_page} records per page...")
    
    # Initialize API
    api = zuercherportal.API(jail, log_level="ERROR")  # Reduce logging for cleaner output
    
    # Warm-up call (not counted in performance)
    print("🔥 Warming up connection...")
    api.inmate_search(records_per_page=1)
    
    # Performance measurement calls
    call_times = []
    total_records = 0
    
    for i in range(num_calls):
        start_time = time.time()
        result = api.inmate_search(records_per_page=records_per_page)
        end_time = time.time()
        
        call_time = end_time - start_time
        call_times.append(call_time)
        
        if result:
            total_records = result.total_record_count
        
        print(f"  📞 Call {i+1}: {call_time:.3f}s")
    
    # Calculate statistics
    avg_time = statistics.mean(call_times)
    min_time = min(call_times)
    max_time = max(call_times)
    median_time = statistics.median(call_times)
    
    print(f"\n📈 Performance Results for {jail.name}:")
    print(f"  ⏱️  Average: {avg_time:.3f}s")
    print(f"  🚀 Fastest: {min_time:.3f}s")
    print(f"  🐌 Slowest: {max_time:.3f}s")
    print(f"  📊 Median:  {median_time:.3f}s")
    print(f"  📋 Total Records Available: {total_records}")
    
    return {
        'jail_name': jail.name,
        'avg_time': avg_time,
        'min_time': min_time,
        'max_time': max_time,
        'median_time': median_time,
        'total_records': total_records
    }


def test_session_reuse_benefit():
    """Test the benefit of session reuse vs creating new API objects"""
    print("\n🔄 Testing Session Reuse Benefits")
    print("=" * 50)
    
    jail = zuercherportal.Jails.AR.BentonCounty()
    num_calls = 3
    
    # Test 1: Reusing same API instance (our optimized approach)
    print("\n✅ Test 1: Reusing API instance (Session Reuse)")
    api_reuse = zuercherportal.API(jail, log_level="ERROR")
    
    reuse_times = []
    for i in range(num_calls):
        start_time = time.time()
        result = api_reuse.inmate_search(records_per_page=5)
        end_time = time.time()
        call_time = end_time - start_time
        reuse_times.append(call_time)
        print(f"  📞 Call {i+1}: {call_time:.3f}s")
    
    avg_reuse = statistics.mean(reuse_times)
    
    # Test 2: Creating new API instance for each call (old approach)
    print("\n❌ Test 2: Creating new API instances (No Session Reuse)")
    
    new_instance_times = []
    for i in range(num_calls):
        start_time = time.time()
        api_new = zuercherportal.API(jail, log_level="ERROR")
        result = api_new.inmate_search(records_per_page=5)
        end_time = time.time()
        call_time = end_time - start_time
        new_instance_times.append(call_time)
        print(f"  📞 Call {i+1}: {call_time:.3f}s")
    
    avg_new = statistics.mean(new_instance_times)
    
    # Calculate improvement
    improvement = ((avg_new - avg_reuse) / avg_new) * 100
    
    print(f"\n🏆 Session Reuse Results:")
    print(f"  🔄 Reused API Average: {avg_reuse:.3f}s")
    print(f"  🆕 New API Average:    {avg_new:.3f}s")
    print(f"  📈 Performance Gain:   {improvement:.1f}% faster")
    
    return improvement


def test_bulk_operations():
    """Test performance with different batch sizes"""
    print("\n📦 Testing Bulk Operation Performance")
    print("=" * 50)
    
    jail = zuercherportal.Jails.AR.BentonCounty()
    api = zuercherportal.API(jail, log_level="ERROR")
    
    batch_sizes = [10, 25, 50, 100]
    
    for batch_size in batch_sizes:
        print(f"\n📊 Testing batch size: {batch_size} records")
        
        times = []
        for i in range(3):  # 3 calls per batch size
            start_time = time.time()
            result = api.inmate_search(records_per_page=batch_size)
            end_time = time.time()
            call_time = end_time - start_time
            times.append(call_time)
        
        avg_time = statistics.mean(times)
        records_per_second = batch_size / avg_time if avg_time > 0 else 0
        
        print(f"  ⏱️  Average time: {avg_time:.3f}s")
        print(f"  🚀 Records/sec: {records_per_second:.1f}")


def main():
    """Main performance testing function"""
    print("🚀 zuercherportal_api Performance Testing")
    print("=" * 50)
    
    # Test multiple jails for comprehensive performance analysis
    test_jails = [
        zuercherportal.Jails.AR.BentonCounty(),
        zuercherportal.Jails.AR.PulaskiCounty(),
        zuercherportal.Jails.CA.SutterCounty(),
    ]
    
    all_results = []
    
    # Performance test for each jail
    for jail in test_jails:
        try:
            result = measure_api_performance(jail, num_calls=5, records_per_page=10)
            all_results.append(result)
        except Exception as e:
            print(f"❌ Error testing {jail.name}: {e}")
    
    # Overall performance summary
    if all_results:
        print(f"\n🎯 Overall Performance Summary")
        print("=" * 50)
        
        avg_times = [r['avg_time'] for r in all_results]
        overall_avg = statistics.mean(avg_times)
        fastest_jail = min(all_results, key=lambda x: x['avg_time'])
        
        print(f"  📊 Overall Average Time: {overall_avg:.3f}s")
        print(f"  🏆 Fastest Jail: {fastest_jail['jail_name']} ({fastest_jail['avg_time']:.3f}s)")
    
    # Test session reuse benefits
    improvement = test_session_reuse_benefit()
    
    # Test bulk operations
    test_bulk_operations()
    
    print(f"\n✅ Performance testing complete!")
    print(f"🎉 Key optimizations implemented:")
    print(f"   • HTTP connection pooling and session reuse")
    print(f"   • Optimized JSON handling (json= vs data=)")
    print(f"   • List comprehensions for data processing")
    print(f"   • Fixed empty records handling bug")
    print(f"   • Reduced memory allocation overhead")
    print(f"   • Session reuse provides {improvement:.1f}% performance gain")


if __name__ == "__main__":
    main()
