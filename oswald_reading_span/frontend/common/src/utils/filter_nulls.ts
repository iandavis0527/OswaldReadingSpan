function notEmpty<T>(value: T | null | undefined): value is T {
    return value !== null;
}

export default function filterNulls<T>(array: (T | null | undefined)[]): T[] {
    return array.filter(notEmpty);
}