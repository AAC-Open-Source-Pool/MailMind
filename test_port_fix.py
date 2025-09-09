#!/usr/bin/env python3
"""
Test script to verify port availability and OAuth setup
"""

import socket
import sys

def test_port_availability():
    """Test if ports 8090-8099 are available"""
    print("🔍 Testing port availability...")
    
    available_ports = []
    for port in range(8090, 8100):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                available_ports.append(port)
                print(f"✅ Port {port} is available")
        except OSError:
            print(f"❌ Port {port} is in use")
    
    if available_ports:
        print(f"\n🎯 Available ports: {available_ports}")
        print(f"🔧 Recommended port: {available_ports[0]}")
        return available_ports[0]
    else:
        print("\n❌ No ports available in range 8090-8099")
        return None

def main():
    print("🚀 Port Availability Test")
    print("=" * 40)
    
    # Test port availability
    available_port = test_port_availability()
    
    if available_port:
        print(f"\n✅ System ready! Use port {available_port} for OAuth")
        print("\n📋 Next steps:")
        print("1. Add these redirect URIs to Google Cloud Console:")
        for port in range(8090, 8100):
            print(f"   http://localhost:{port}/")
        print("2. Run: python main.py")
    else:
        print("\n❌ No available ports found")
        print("💡 Try closing other applications or restarting your system")

if __name__ == "__main__":
    main()
