export enum AgeRanges {
  ZERO_THREE = "0-3",
  TWO_SIX = "3-6",
  SIX_PLUS = "6-9",
}

export type group = {
  group_id: string;
  organization_id: string;
  name: string;
  age_range: AgeRanges;
};

export type groups = [group];

export const GROUP: group = {
    group_id: "",
    organization_id: "",
    name: "",
    age_range: AgeRanges.ZERO_THREE,
};

export const GROUPS: groups = [GROUP];

