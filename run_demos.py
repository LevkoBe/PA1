from isolation_levels import read_uncommitted_demo, read_committed_demo, repeatable_read_demo, serializable_demo

def main():
    while True:
        print("\nChoose a demo to run:")
        print("1: READ UNCOMMITTED")
        print("2: READ COMMITTED")
        print("3: REPEATABLE READ")
        print("4: SERIALIZABLE")
        print("5: Exit")
        
        choice = input("Enter the number of your choice: ")

        if choice == '1':
            read_uncommitted_demo()
        elif choice == '2':
            read_committed_demo()
        elif choice == '3':
            repeatable_read_demo()
        elif choice == '4':
            serializable_demo()
        else:
            print("Exiting.")
            break

if __name__ == "__main__":
    main()
