#!/usr/bin/env python3
"""
Enhanced Email Processing Pipeline with Google Calendar Integration
Fetches emails, processes them with AI, and creates calendar events for event-based emails
"""

from enhanced_email_processor import enhanced_processor

def main():
    """Main email processing pipeline"""
    print("🚀 Starting Enhanced Email Processing Pipeline...")
    print("=" * 60)
    
    # For demo purposes, use a default user ID
    # In production, this would come from user authentication
    user_id = "demo_user_123"
    
    try:
        # Step 1: Authenticate with Google APIs
        print("🔐 Authenticating with Google APIs...")
        if not enhanced_processor.authenticate_google_apis(user_id):
            print("❌ Authentication failed. Exiting.")
            return
        
        # Step 2: Fetch unread emails
        print("\n📧 Fetching unread emails...")
        emails = enhanced_processor.fetch_unread_emails(max_emails=5)  # Process 5 emails at a time
        
        if not emails:
            print("📭 No unread emails found.")
            return
        
        # Step 3: Process emails with AI
        print("\n🤖 Processing emails with AI...")
        processed_emails, event_emails = enhanced_processor.process_emails_with_ai(emails)
        
        # Step 4: Create calendar events for event-based emails
        print("\n📅 Creating calendar events...")
        created_events = enhanced_processor.create_calendar_events(event_emails)
        
        # Step 5: Mark emails as read
        print("\n✅ Marking emails as read...")
        email_ids = [email['id'] for email in emails]
        enhanced_processor.mark_emails_as_read(email_ids)
        
        # Step 6: Generate summary report
        print("\n📊 Generating summary report...")
        report = enhanced_processor.generate_summary_report(processed_emails, event_emails, created_events)
        
        # Step 7: Display results
        print("\n" + "=" * 60)
        print("📋 PROCESSING SUMMARY")
        print("=" * 60)
        
        if report:
            summary = report['summary']
            print(f"📧 Total emails processed: {summary['total_emails_processed']}")
            print(f"🚫 Spam detected: {summary['spam_detected']}")
            print(f"📅 Events extracted: {summary['events_extracted']}")
            print(f"✅ Calendar events created: {summary['calendar_events_created']}")
            print(f"📝 Regular emails with summaries: {summary.get('regular_emails', 0)}")
            
            if created_events:
                print("\n📅 CREATED CALENDAR EVENTS:")
                print("-" * 40)
                for event in created_events:
                    print(f"📅 {event['event_title']}")
                    print(f"   📧 Email: {event['email_subject']}")
                    print(f"   🔗 Calendar: {event['calendar_link']}")
                    print()
            
            # Display event-based emails
            if event_emails:
                print("\n📧 EVENT-BASED EMAILS:")
                print("-" * 40)
                for email in event_emails:
                    event_details = email.get('analysis', {}).get('event_details', {})
                    print(f"📧 {email['subject']}")
                    print(f"   📅 Event: {event_details.get('title', 'N/A')}")
                    print(f"   🕒 Time: {event_details.get('start_time', 'N/A')}")
                    print(f"   📍 Location: {event_details.get('location', 'N/A')}")
                    print()
            
            # Display regular (non-spam, non-event) emails with summaries
            regular_emails = [email for email in processed_emails 
                            if not email.get('spam_detected', False) and not email.get('event_extracted', False)]
            
            if regular_emails:
                print("\n📧 REGULAR EMAILS (with summaries):")
                print("-" * 40)
                for email in regular_emails:
                    print(f"📧 {email['subject']}")
                    print(f"   👤 From: {email.get('sender', 'Unknown')}")
                    print(f"   📝 Summary: {email.get('summary', 'No summary available')}")
                    print()
        
        print("🎉 Email processing completed successfully!")
        
    except Exception as e:
        print(f"❌ Error in main pipeline: {e}")

if __name__ == '__main__':
    main()
