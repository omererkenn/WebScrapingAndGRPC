from product_pb2_grpc import ScrapeServiceServicer
import grpc
import product_pb2
import product_pb2_grpc
from scraper import scrape_amazon_bestsellers
from concurrent.futures import ThreadPoolExecutor

class ScrapeService(product_pb2_grpc.ScrapeServiceServicer):
   def ProductResponse(self, request, context):
      return super().ProductResponse(request , context=scrape_amazon_bestsellers)
 

     
       
def serve():
   server = grpc.server(ThreadPoolExecutor(max_workers=10))
   product_pb2_grpc.add_ScrapeServiceServicer_to_server(ScrapeService(), server)
   server.add_insecure_port("[::]:8080")
   server.start()
   server.wait_for_termination()


if __name__ == "__main__":
   print("running the gRPC server")
   serve()
