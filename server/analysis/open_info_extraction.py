from stanza.server import CoreNLPClient
from stanza.server.client import StartServer
import logging
import time
import requests

class OpenInformationExtraction:
    def __init__(self, max_retries=3):
        """
        Initialize OpenIE client - connects to existing CoreNLP server
        
        Args:
            max_retries (int): Maximum connection retry attempts
        """
        self.max_retries = max_retries
        self.client = None
        self._connect_with_retry()
    
    def _connect_with_retry(self):
        """Connect to CoreNLP server with retry logic"""
        for attempt in range(self.max_retries):
            try:
                # First check if server is accessible
                response = requests.get('http://localhost:9000/', timeout=2)
                if response.status_code != 200:
                    raise Exception(f"CoreNLP server returned status {response.status_code}")
                
                # Connect to existing server (don't start a new one!)
                self.client = CoreNLPClient(
                    start_server=StartServer.DONT_START,
                    endpoint='http://localhost:9000',
                    timeout=60000,
                    annotators=['openie'],
                    output_format='serialized'
                )
                print("CoreNLP client connected successfully")
                return
                
            except Exception as e:
                print(f"CoreNLP connection attempt {attempt + 1}/{self.max_retries} failed: {e}")
                if attempt < self.max_retries - 1:
                    wait_time = (attempt + 1) * 2  # Exponential backoff
                    print(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    print("Failed to connect to CoreNLP after all retries")
                    raise Exception("CoreNLP server unavailable")
    
    def _check_connection(self):
        """Check if CoreNLP is still accessible"""
        try:
            response = requests.get('http://localhost:9000/', timeout=1)
            return response.status_code == 200
        except:
            return False
    
    def generate_triples(self, text, retry_on_failure=True):
        """
        Extract triples from text using OpenIE with automatic retry
        
        Args:
            text (str): Input text to extract triples from
            retry_on_failure (bool): Whether to retry on connection failures
            
        Returns:
            list: List of tuples (subject, relation, object)
        """
        if not text or not text.strip():
            return []
        
        # Attempt with retry logic
        for attempt in range(self.max_retries if retry_on_failure else 1):
            try:
                # Check if we need to reconnect
                if self.client is None:
                    print("Client disconnected, attempting to reconnect...")
                    self._connect_with_retry()
                
                # Annotate text
                ann = self.client.annotate(text)
                
                triples = []
                
                # Extract triples from each sentence
                for sentence in ann.sentence:
                    for triple in sentence.openieTriple:
                        subject = triple.subject
                        relation = triple.relation
                        obj = triple.object
                        
                        # Clean and normalize
                        subject = subject.strip()
                        relation = relation.strip()
                        obj = obj.strip()
                        
                        if subject and relation and obj:
                            triples.append((subject, relation, obj))
                
                return triples
                
            except Exception as e:
                error_msg = str(e)
                is_connection_error = (
                    "Connection refused" in error_msg or 
                    "Max retries exceeded" in error_msg or
                    "Failed to establish" in error_msg or
                    "Connection reset" in error_msg
                )
                
                if is_connection_error and retry_on_failure and attempt < self.max_retries - 1:
                    print(f"CoreNLP connection lost (attempt {attempt + 1}/{self.max_retries}): {e}")
                    
                    # Mark client as disconnected
                    self.client = None
                    
                    # Check if server is still up
                    if not self._check_connection():
                        print("CoreNLP server appears to be down")
                        wait_time = (attempt + 1) * 3
                        print(f"Waiting {wait_time}s for server recovery...")
                        time.sleep(wait_time)
                    else:
                        # Server is up but connection failed, try reconnecting
                        time.sleep(1)
                        try:
                            self._connect_with_retry()
                        except:
                            print("Reconnection failed, will retry on next attempt")
                else:
                    # Non-connection error or max retries reached
                    print(f"Error generating triples: {e}")
                    return []
        
        # All retries exhausted
        print(f"Failed to generate triples after {self.max_retries} attempts")
        return []
    
    def __del__(self):
        """Cleanup - but don't stop the server since we didn't start it"""
        pass