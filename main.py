import python_actr as actr


class TowerWorld(actr.Model):
    goal = actr.Buffer()
    retrieval = actr.Buffer()
    dm = actr.Memory(retrieval)

    towers = {'A': [], 'B': [], 'C': []}

    def init(self):
        self.towers = {'A': [3, 2, 1], 'B': [], 'C': []}
        self.goal.set('source A dest C temp B disk 3')

    def print_towers(self):
        print("Current Towers:")
        for tower, disks in self.towers.items():
            print(f"{tower}: {disks}")
        print("")  # Add a new line for better readability

    def move(self, source, dest, temp, disk):
        if disk == 1:
            print(f'Move disk 1 from {source} to {dest}')
            self.towers[dest].append(self.towers[source].pop())
            self.print_towers()
            self.goal.set(f'source {source} dest {dest} temp {temp} disk 0')
        else:
            self.goal.set(f'source {source} dest {temp} temp {dest} disk {disk - 1}')
            self.move(source, temp, dest, disk - 1)
            print(f'Move disk {disk} from {source} to {dest}')
            self.towers[dest].append(self.towers[source].pop())
            self.print_towers()
            self.move(temp, dest, source, disk - 1)

    def production(self, source='A', dest='C', temp='B', disk='3'):
        disk = int(disk)  # Ensure disk is an integer
        if disk > 0:
            self.move(source, dest, temp, disk)
        else:
            print('All moves complete')


model = TowerWorld()
model.init()
model.production()

actr.run("production")
