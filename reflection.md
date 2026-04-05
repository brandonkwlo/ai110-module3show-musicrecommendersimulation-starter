# Profile Comparison Reflections

## pop_party vs rock_workout

Both profiles want high energy and no acoustic — but they diverge on genre and mood. pop_party (energy 0.85, mood "happy") surfaces Sunrise City at #1 with a clean genre + mood + energy triple match. rock_workout (energy 0.92, mood "intense") surfaces Storm Runner at #1 for the same reason. What's telling is that Gym Hero (pop, intense) appears at #2 for rock_workout via mood match alone, even though the genre is wrong — showing that when two out of three semantic signals align, a song can still rank very high. The scores are close in structure but the #2–#5 results are completely different, which makes sense: high-energy pop and high-energy rock share an energy profile but live in separate parts of the catalog.

## lofi_focus vs ambient_unwind

These two profiles are the most similar on paper — both prefer low energy and like acoustic — but their genre and mood differ (lofi/focused vs ambient/chill). lofi_focus returns Focus Flow at 11.17 with a perfect energy match and all four scoring signals firing. ambient_unwind returns Spacewalk Thoughts at 11.38, also a perfect energy match. The interesting difference shows up at #2 and #3: both profiles return Library Rain and Midnight Coding, but in a different order, because those songs match the "chill" mood of ambient_unwind but not the "focused" mood of lofi_focus. This confirms the mood bonus is doing real work — it reshuffles songs that are otherwise nearly identical in energy and acousticness.

## lofi_focus vs misspelled_mood

These two profiles are identical except misspelled_mood uses "Focus" instead of "focused" — a one-character case difference. The top 3 songs are the same in both outputs, but Focus Flow drops from 11.17 to 8.17 (a loss of exactly 3.00 points — the mood bonus). The ranking held because energy and genre were strong enough to keep the right songs on top, but the scores are meaningfully deflated. This comparison demonstrates that the system has no resilience to input formatting errors: it doesn't warn the user, doesn't suggest a correction, and silently produces a worse result.

## rock_workout vs acoustic_trap

Both profiles want rock/intense at high energy, but acoustic_trap adds likes_acoustic=True. This is a conflicting preference — rock songs in the dataset have very low acousticness values. Storm Runner still wins both runs, but drops from 10.86 to 9.99. More importantly, the acoustic bonus across all songs is nearly zero (Storm Runner earns +0.15 instead of the electric +0.90), meaning the acoustic preference is being registered but never rewarded. This reveals a real bias: the system cannot satisfy a user who genuinely wants acoustic rock because the dataset doesn't contain it — and the scoring doesn't flag that the preference went unmet.

## pop_party vs flatline

Both profiles want pop/happy, but flatline targets energy 0.5 instead of 0.85. The same song — Sunrise City — ranks #1 for both, but with a lower score (9.54 vs 10.70) because its actual energy of 0.82 is much closer to pop_party's 0.85 than to flatline's 0.5. The bigger change is in #2–#5: flatline's middle-energy target pulls songs like Signal in the Fog and Velvet Sunrise into the top 5, which never appear for pop_party. This shows the energy parameter is actively reshaping the long tail of results even when the top recommendation stays the same.

## genre_ghost vs ghost_profile

Both profiles name a genre not in the dataset ("jazz"), so neither ever receives the +3.00 genre bonus. genre_ghost still gets the mood bonus for "happy" (Sunrise City, Rooftop Lights rise to the top). ghost_profile has both genre and mood missing, so its entire ranking is determined by energy proximity and acousticness alone — Coffee Shop Stories wins at 7.82 purely because its energy (0.37) and acousticness (0.89) match the target numerically. Comparing these two shows how much semantic meaning is lost when the genre/mood signals disappear: genre_ghost still feels somewhat intentional, but ghost_profile's output could belong to any user with energy≈0.5 and likes_acoustic=True, regardless of what music they actually care about.
