import { generateSentenceSets } from "./sentences";
import { shuffle } from "rspan_common/lib/utils/array_shuffle";

test("ensure varying set lengths", () => {
  let practice_set = generateSentenceSets([3, 5, 7]);
  expect(practice_set.length).toBe(3);
  expect(practice_set[0].length).toBe(3);
  expect(practice_set[1].length).toBe(5);
  expect(practice_set[2].length).toBe(7);
});

test("ensure set wraps if too many requested", () => {
  let practice_set = generateSentenceSets([82, 82, 82]);
  expect(practice_set.length).toBe(3);
  expect(practice_set[0].length).toBe(82);
  expect(practice_set[1].length).toBe(82);
  expect(practice_set[2].length).toBe(82);
  expect(practice_set[0][practice_set[0].length - 1]).toStrictEqual(
    practice_set[0][0]
  );
  expect(practice_set[1][practice_set[1].length - 1]).toStrictEqual(
    practice_set[1][0]
  );
  expect(practice_set[2][practice_set[2].length - 1]).toStrictEqual(
    practice_set[2][0]
  );
});

test("ensure no duplicates generated", () => {
  for (let _ = 0; _ < 50; _++) {
    let set_lengths = shuffle([4, 4, 5, 5, 6, 6]);
    let practice_set = generateSentenceSets(set_lengths);
    let encountered_problems = [];

    expect(practice_set.length).toBe(6);

    for (let i = 0; i < practice_set.length; i++) {
      let set = practice_set[i];

      for (let j = 0; j < set.length; j++) {
        let problem = set[j];
        // expect(encountered_problems).toEqual(expect.not.arrayContaining([problem]));
        encountered_problems.push(problem);
      }
    }

    for (let i = 0; i < encountered_problems.length; i++) {
      for (let j = 0; j < encountered_problems.length; j++) {
        if (j === i) continue;
        let problemOne = encountered_problems[i];
        let problemTwo = encountered_problems[j];
        expect(problemOne).not.toStrictEqual(problemTwo);
      }
    }
  }
});

test("ensure zero set lengths", () => {
  let practice_sets = generateSentenceSets([0]);

  expect(practice_sets.length).toBe(1);
  expect(practice_sets[0].length).toBe(0);
});

test("ensure empty set length", () => {
  let practice_sets = generateSentenceSets([]);
  expect(practice_sets.length).toBe(0);
});
