from dotenv import load_dotenv

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import (
    openai,
    noise_cancellation,
)
from openai.types.beta.realtime.session import  InputAudioTranscription, TurnDetection

load_dotenv()


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions="be talkative")


async def entrypoint(ctx: agents.JobContext):
    await ctx.connect()

    session = AgentSession(
        llm=openai.realtime.RealtimeModel(
	    model="gpt-4o-realtime-preview-2024-12-17",
            voice="coral",
	    api_key="sk-proj-----------------------------------",
	    input_audio_transcription=InputAudioTranscription(model="gpt-4o-transcribe", language="en", prompt="expect informal english"),
	    temperature=1.0,
	    turn_detection=TurnDetection(type="semantic_vad", eagerness="auto", create_response=True, interrupt_response=False,),
        ),
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
    )

    await session.generate_reply(
        instructions="Start the act immediatly"
    )


if __name__ == "__main__":

    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
