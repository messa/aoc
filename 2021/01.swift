import Foundation
let input = try String(contentsOfFile: "01_input.txt", encoding: String.Encoding.utf8)
let numbers = input.split(separator: "\n").map { Int($0)! }
func partOne() -> Int {
    zip(numbers, numbers.dropFirst())
        .filter { $0 < $1 }
        .count
}
print(partOne())
