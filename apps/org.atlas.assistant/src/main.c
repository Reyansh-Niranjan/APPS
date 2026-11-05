/**
 * @file main.c
 * @brief Gemini Live (Extended Thinking Communicator) Application Source
 *
 * Implements the dual-pane cybernetic HUD, audio capture trigger,
 * and SSE thinking token processor for Atlas OS.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <stdint.h>

/* System dimensions */
#define SCREEN_W   320
#define SCREEN_H   240

/* Communicator States */
typedef enum {
    AI_STATE_STANDBY = 0,
    AI_STATE_LISTENING,
    AI_STATE_UPLOADING,
    AI_STATE_THINKING,
    AI_STATE_RESPONDING,
    AI_STATE_DONE,
    AI_STATE_ERROR
} ai_communicator_state_t;

typedef struct {
    ai_communicator_state_t state;
    char thoughts[1024];
    char answer[1024];
    int mic_level;
    int scroll_offset;
    char status_line[64];
} ai_session_t;

static ai_session_t s_session;

void app_entry(void)
{
    printf("[Gemini Live] Starting Gemini 3.8 Extended Thinking Communicator...\n");
    memset(&s_session, 0, sizeof(s_session));
    s_session.state = AI_STATE_STANDBY;
    snprintf(s_session.status_line, sizeof(s_session.status_line), "Ready - Hold [A] to Speak");
}

void app_process_audio_chunk(const int16_t *samples, size_t count)
{
    if (s_session.state != AI_STATE_LISTENING || !samples || count == 0) return;

    /* Compute simple RMS level for the sound-reactive VU meter */
    int32_t sum = 0;
    for (size_t i = 0; i < count; i += 8) {
        int32_t val = samples[i];
        if (val < 0) val = -val;
        sum += val;
    }
    s_session.mic_level = (int)(sum / (count / 8));
}

void app_on_token_received(bool is_thought, const char *token)
{
    if (!token) return;

    if (is_thought) {
        s_session.state = AI_STATE_THINKING;
        snprintf(s_session.status_line, sizeof(s_session.status_line), "Gemini is Reasoning...");
        size_t cur = strlen(s_session.thoughts);
        size_t rem = sizeof(s_session.thoughts) - cur - 1;
        strncat(s_session.thoughts, token, rem);
    } else {
        s_session.state = AI_STATE_RESPONDING;
        snprintf(s_session.status_line, sizeof(s_session.status_line), "Streaming Answer...");
        size_t cur = strlen(s_session.answer);
        size_t rem = sizeof(s_session.answer) - cur - 1;
        strncat(s_session.answer, token, rem);
    }
}
