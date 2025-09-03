from typing import Any
import requests
from game.sigs import APP_VERSION_SIG


def content_length(data: dict[Any, Any]) -> int:
    return len(str(data))


class GameEndpoint:
    def __init__(
        self,
        endpoint: str,
        ticket: str,
        further_json: dict[str, Any] | None = None,
    ) -> None:
        self.ticket: str = ticket
        self.url: str = (
            f"https://www.simplicialsoftware.com/api/account/{endpoint}"
        )
        self.further_json: dict[str, Any] | None = further_json

    def execute(self) -> dict[Any, Any] | Exception:
        default_json: dict[str, str | int] = {
            "Ticket": self.ticket,
            "Game": "Nebulous",
            "Version": APP_VERSION_SIG,
        }
        if self.further_json:
            default_json |= self.further_json
        headers: dict[str, str] = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": str(content_length(default_json)),
        }
        try:
            r = requests.post(self.url, data={**default_json}, headers=headers)
            j = r.json()
            return Exception(j["Error"]) if j["Error"] else j
        except Exception as e:
            return e


class JDKaYIIScQ(GameEndpoint):
    def __init__(self, ticket: str, region: str) -> None:
        super().__init__(
            "JDKaYIIScQ",
            ticket,
            {
                "region": region,
                "vPJFmN6rEt": "Local integrity API failure null",
            },
        )


class GetRPGResetToken(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("GetRPGResetToken", ticket)


class JoinClan(GameEndpoint):
    def __init__(self, ticket: str, clan_id: int) -> None:
        super().__init__("JoinClan", ticket, {"clanID": clan_id})


class GetClanMembers(GameEndpoint):
    def __init__(
        self,
        ticket: str,
        clan_name: str,
        start_index: int,
        count: int,
        search: str,
    ) -> None:
        super().__init__(
            "GetClanMembers",
            ticket,
            {
                "ClanName": clan_name,
                "StartIndex": start_index,
                "Count": count,
                "Search": search,
            },
        )


class LeaveTeam(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("LeaveTeam", ticket)


class GetPurchasePrices(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("GetPurchasePrices", ticket)


class GetArenaTeamPurchaseInfo(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("GetArenaTeamPurchaseInfo", ticket)


class DeleteCustomSkin(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("DeleteCustomSkin", ticket)


class GetActiveEffects(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("GetActiveEffects", ticket)


class Unblock(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("Unblock", ticket)


class GetPacks(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("GetPacks", ticket)


class JoinTeam(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("JoinTeam", ticket)


class GetClanStats(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("GetClanStats", ticket)


class GetTourneyInfo(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("GetTourneyInfo", ticket)


class GetFriends(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("GetFriends", ticket)


class UpdateClanInfo(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("UpdateClanInfo", ticket)


class RedeemPurchase(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("RedeemPurchase", ticket)


class GetOneoffPurchases(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("GetOneoffPurchases", ticket)


class GetClanJoinRequests(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("GetClanJoinRequests", ticket)


class DemoteClanMember(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("DemoteClanMember", ticket)


class RequestCommunitySkinData(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("RequestCommunitySkinData", ticket)


class SetName(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("SetName", ticket)


class SetClanPermissions(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("SetClanPermissions", ticket)


class SetClanDescriptionColors(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("SetClanDescriptionColors", ticket)


class GetClanXPLeaderBoard(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("GetClanXPLeaderBoard", ticket)


class GetClanWarHistory(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("GetClanWarHistory", ticket)


class RemoveFriend(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("RemoveFriend", ticket)


class PromoteClanMember(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("PromoteClanMember", ticket)


class RemoveClanAlly(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("RemoveClanAlly", ticket)


class DeleteMail(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("DeleteMail", ticket)


class GetPlayerStats(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("GetPlayerStats", ticket)


class UpdateMailNotificationSetting(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("UpdateMailNotificationSetting", ticket)


class RemoveClanEnemy(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("RemoveClanEnemy", ticket)


class GetDailyQuestDetails(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("GetDailyQuestDetails", ticket)


class MoveSkin(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("MoveSkin", ticket)


class GetClanWarLeaderBoards(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("GetClanWarLeaderBoards", ticket)


class SendTeamInvite(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("SendTeamInvite", ticket)


class SendMail(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("SendMail", ticket)


class GetArenaHistory(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("GetArenaHistory", ticket)


class GetMailList(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("GetMailList", ticket)


class DeleteAccount(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("DeleteAccount", ticket)


class LeaveClan(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("LeaveClan", ticket)


class GetSkinData(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("GetSkinData", ticket)


class GetSkinIDs(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("GetSkinIDs", ticket)


class SetClanProfileBackgroundColor(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("SetClanProfileBackgroundColor", ticket)


class UpdateClanProfile(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("UpdateClanProfile", ticket)


class ResetDQ(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("ResetDQ", ticket)


class GetClanRelations(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("GetClanRelations", ticket)


class AddClanAlly(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("AddClanAlly", ticket)


class GetClanInvites(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("GetClanInvites", ticket)


class GetTourneyLB(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("GetTourneyLB", ticket)


class GetClanBans(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("GetClanBans", ticket)


class GetPlayerProfile(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("GetPlayerProfile", ticket)


class Report(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("Report", ticket)


class GetClientConfig(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("GetClientConfig", ticket)


class GetMyPurchases(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("GetMyPurchases", ticket)


class CheckIn(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("CheckIn", ticket)


class SendFirebaseToken(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("SendFirebaseToken", ticket)


class UnBan(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("UnBan", ticket)


class GetClanAudit(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("GetClanAudit", ticket)


class SetClanColors(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("SetClanColors", ticket)


class RandomizeDQ(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("RandomizeDQ", ticket)


class GetMods(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("GetMods", ticket)


class SetClanName(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("SetClanName", ticket)


class GetClanHouseInfo(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("GetClanHouseInfo", ticket)


class GetArenaTokenStatus(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("GetArenaTokenStatus", ticket)


class GetHighScores(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("GetHighScores", ticket)


class BFF(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("BFF", ticket)


class GetAccountInfoForMod(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("GetAccountInfoForMod", ticket)


class CreateClan(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("CreateClan", ticket)


class SetPlayerProfileColors(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("SetPlayerProfileColors", ticket)


class SetPlayerProfileBackgroundColor(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("SetPlayerProfileBackgroundColor", ticket)


class GetClanInfo(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("GetClanInfo", ticket)


class RejectClanInvite(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("RejectClanInvite", ticket)


class CoinPurchase(GameEndpoint):
    def __init__(
        self, ticket: str, item_type: str, item_id: int, expected_price: int
    ) -> None:
        super().__init__(
            "CoinPurchase",
            ticket,
            {
                "ItemType": item_type,
                "ItemID": item_id,
                "ExpectedPrice": expected_price,
            },
        )


class CreateTeam(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("CreateTeam", ticket)


class SetCommunitySkinFavorite(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("SetCommunitySkinFavorite", ticket)


class MarkMailUnread(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("MarkMailUnread", ticket)


class UploadSkin(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("UploadSkin", ticket)


class ReadMail(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("ReadMail", ticket)


class RemoveSkinFromCommunity(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("RemoveSkinFromCommunity", ticket)


class SetPlayerProfile(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("SetPlayerProfile", ticket)


class AddClanEnemy(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("AddClanEnemy", ticket)


class UpdateSettings(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("UpdateSettings", ticket)


class GetXPLeaderBoard(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("GetXPLeaderBoard", ticket)


class GetTeamArenaLeaderboards(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("GetTeamArenaLeaderboards", ticket)


class SetProfileVisibility(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("SetProfileVisibility", ticket)


class CancelSkinUpload(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("CancelSkinUpload", ticket)


class GetSpinInfo(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("GetSpinInfo", ticket)


class GetTeamList(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("GetTeamList", ticket)


class SendClanInvite(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("SendClanInvite", ticket)


class GetCoinPurchases(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("GetCoinPurchases", ticket)


class GetAlerts(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("GetAlerts", ticket)


class SignOutAllDevices(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("SignOutAllDevices", ticket)


class AnswerClanRequest(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("AnswerClanRequest", ticket)


class RemoveTeamMember(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("RemoveTeamMember", ticket)


class GetActiveClanEffects(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("GetActiveClanEffects", ticket)


class GetClanInvitees(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("GetClanInvitees", ticket)


class BlockMail(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("BlockMail", ticket)


class RemoveClanMember(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("RemoveClanMember", ticket)


class AddFriend(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("AddFriend", ticket)


class GetCustomSkinStatus(GameEndpoint):
    def __init__(self, ticket: str) -> None:
        super().__init__("GetCustomSkinStatus", ticket)
