# Ultra-simple web test version
import asyncio

print("Starting minimal test...")

async def main():
    print("In main function")
    
    try:
        import pygame
        print("Pygame imported successfully")
        
        pygame.init()
        print("Pygame initialized")
        
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Test")
        print("Display created")
        
        clock = pygame.time.Clock()
        print("Clock created")
        
        frame = 0
        while frame < 60:  # Run for 60 frames only
            frame += 1
            print(f"Frame {frame}")
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            
            screen.fill((50, 50, 150))  # Blue background
            
            pygame.display.flip()
            clock.tick(60)
            await asyncio.sleep(0)
            
        print("Test completed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
