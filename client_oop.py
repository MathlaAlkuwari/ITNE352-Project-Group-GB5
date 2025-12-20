class MenuDisplay:
    
    COUNTRIES = ['au', 'ca', 'jp', 'ae', 'sa', 'kr', 'us', 'ma']
    LANGUAGES = ['ar', 'en']
    CATEGORIES = ['business', 'general', 'health', 'science', 'sports', 'technology']

    @staticmethod
    def print_header(title):
        print("\n" + "=" * 60)
        print(f"  {title}")
        print("=" * 60)
    
    @staticmethod
    def display_main_menu():
        """Display the main menu"""
        MenuDisplay.print_header("MAIN MENU")
        print("1. Search for headlines")
        print("2. List of sources")
        print("3. Quit")
        print("-" * 60)
    
    @staticmethod
    def display_headlines_menu():
        """Display headlines menu"""
        MenuDisplay.print_header("HEADLINES MENU")
        print("1. Search by keyword")
        print("2. Search by category")
        print("3. Search by country")
        print("4. List all headlines")
        print("5. Back to main menu")
        print("-" * 60)
    
    @staticmethod
    def display_sources_menu():
        """Display sources menu"""
        MenuDisplay.print_header("SOURCES MENU")
        print("1. Search by category")
        print("2. Search by country")
        print("3. Search by language")
        print("4. List all sources")
        print("5. Back to main menu")
        print("-" * 60)
    
    @staticmethod
    def display_categories():
        """Display available categories"""
        print("\nAvailable categories:")
        for i, cat in enumerate(MenuDisplay.CATEGORIES, 1):
            print(f"{i}. {cat}")
    
    @staticmethod
    def display_countries():
        """Display available countries"""
        print("\nAvailable countries:")
        
        countries_map = {
            'au': 'Australia',
            'ca': 'Canada',
            'jp': 'Japan',
            'ae': 'UAE',
            'sa': 'Saudi Arabia',
            'kr': 'South Korea',
            'us': 'USA',
            'ma': 'Morocco'
        }
        for i, code in enumerate(MenuDisplay.COUNTRIES, 1):
            print(f"{i}. {countries_map[code]} ({code})")
    
    @staticmethod
    def display_languages():
        """Display available languages"""
        print("\nAvailable languages:")
        print("1. Arabic (ar)")
        print("2. English (en)")


# ============================================================
# NewsDisplay Class - Showing news
# ============================================================

class NewsDisplay:
    """
    This class is responsible for displaying news and source data.
    It is separated from MenuDisplay to follow single-responsibility principle.
    """
    
    @staticmethod
    def display_headlines_list(articles):
        """
        Display list of headlines
        
        Parameters:
            articles: list containing news articles
        
        Returns:
            list: Only first 15 headlines
        """
        MenuDisplay.print_header("HEADLINES")
        
        if not articles:
            print("No articles found.")
            return []
        
        for i, article in enumerate(articles[:15], 1):
            print(f"\n{i}. Title: {article.get('title', 'N/A')}")
            print(f"   Source: {article.get('source', {}).get('name', 'N/A')}")
            print(f"   Author: {article.get('author', 'N/A')}")
            print("-" * 60)
        
        return articles[:15]
    
    @staticmethod
    def display_headline_details(article):
        """
        Display details of a single news article
        
        Parameters:
            article: dictionary containing news data
        """
        MenuDisplay.print_header("HEADLINE DETAILS")
        print(f"Title: {article.get('title', 'N/A')}")
        print(f"Source: {article.get('source', {}).get('name', 'N/A')}")
        print(f"Author: {article.get('author', 'N/A')}")
        print(f"Description: {article.get('description', 'N/A')}")
        print(f"URL: {article.get('url', 'N/A')}")
        
        published_at = article.get('publishedAt', 'N/A')
        if published_at != 'N/A':
            try:
                dt = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                print(f"Published Date: {dt.strftime('%Y-%m-%d')}")
                print(f"Published Time: {dt.strftime('%H:%M:%S')}")
            except:
                print(f"Published: {published_at}")
        print("=" * 60)
    
    @staticmethod
    def display_sources_list(sources):
        """
        Display list of sources
        
        Parameters:
            sources: list of sources
        
        Returns:
            list: first 15 sources
        """
        MenuDisplay.print_header("SOURCES")
        
        if not sources:
            print("No sources found.")
            return []
        
        for i, source in enumerate(sources[:15], 1):
            print(f"{i}. {source.get('name', 'N/A')}")
            print("-" * 60)
        
        return sources[:15]
    
    @staticmethod
    def display_source_details(source):
        """
        Display source details
        
        Parameters:
            source: dictionary of source information
        """
        MenuDisplay.print_header("SOURCE DETAILS")
        print(f"Name: {source.get('name', 'N/A')}")
        print(f"Country: {source.get('country', 'N/A').upper()}")
        print(f"Description: {source.get('description', 'N/A')}")
        print(f"URL: {source.get('url', 'N/A')}")
        print(f"Category: {source.get('category', 'N/A')}")
        print(f"Language: {source.get('language', 'N/A')}")
        print("=" * 60)


# ============================================================
# NewsClient Class - Main Client
# ============================================================

class NewsClient:
    """
    Main Client class
    Handles communication with the server and user interaction
    """
    
    def __init__(self, host='127.0.0.1', port=5000):
        """
        Constructor
        
        Parameters:
            host: server host (localhost)
            port: server port
        """
        self.host = host
        self.port = port
        self.socket = None
        self.protocol = Protocol()
        self.client_name = None
        self.menu_display = MenuDisplay()
        self.news_display = NewsDisplay()
    
    def send(self, message):
        """Send message to server"""
        return self.protocol.send_message(self.socket, message)
    
    def receive(self):
        """Receive message from server"""
        return self.protocol.receive_message(self.socket)
